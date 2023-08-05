# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Training functions."""
import copy
import pickle
import time
import torch

from contextlib import nullcontext

from azureml.contrib.automl.dnn.vision.classification.common.constants import TrainingLiterals
from azureml.contrib.automl.dnn.vision.classification.common.transforms import (_get_common_train_transforms,
                                                                                _get_common_valid_transforms)
from azureml.contrib.automl.dnn.vision.classification.io.read.dataloader import _get_data_loader
from azureml.contrib.automl.dnn.vision.classification.models import ModelFactory
from azureml.contrib.automl.dnn.vision.classification.trainer.criterion import _get_criterion
from azureml.contrib.automl.dnn.vision.common import distributed_utils, utils
from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.common.artifacts_utils import save_model_checkpoint, write_artifacts
from azureml.contrib.automl.dnn.vision.common.constants import MetricsLiterals, \
    SettingsLiterals as CommonSettingsLiterals, TrainingCommonSettings, TrainingLiterals as CommonTrainingLiterals
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException, AutoMLVisionDataException
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter
from azureml.contrib.automl.dnn.vision.common.trainer.lrschedule import LRSchedulerUpdateType, setup_lr_scheduler
from azureml.contrib.automl.dnn.vision.common.trainer.optimize import setup_optimizer
from azureml.contrib.automl.dnn.vision.metrics import ClassificationMetrics
from azureml.contrib.automl.dnn.vision.classification.io.write.score_script_utils import write_scoring_script

logger = get_logger(__name__)


def train_model(dataset_wrapper, valid_dataset, settings, train_transforms=None, valid_transforms=None,
                device=None, output_dir=None, azureml_run=None, save_checkpoints=False):
    """
    :param dataset_wrapper: datasetwrapper object for training
    :type dataset_wrapper: azureml.automl.contrib.dnn.vision.io.read.DatasetWrapper
    :param valid_dataset: datasetwrapper object for validation
    :type valid_dataset: azureml.contrib.automl.dnn.vision.io.read.DatasetWrapper
    :param settings: dictionary containing settings for training
    :type settings: dict
    :param train_transforms: transformation function to apply to a pillow image object
    :type train_transforms: function
    :param valid_transforms: transformation function to apply to a pillow image object
    :type valid_transforms: function
    :param device: device where model should be run (usually "cpu" or "cuda:0" if it is the first gpu)
    :type device: str
    :param output_dir: output directory
    :type output_dir: str
    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.Run
    :param save_checkpoints: If True, the checkpoints from each epoch are saved. If False, only the best one.
    :type save_checkpoints: bool
    """
    # Extract relevant parameters from training settings
    task_type = settings[CommonSettingsLiterals.TASK_TYPE]
    model_name = settings[CommonSettingsLiterals.MODEL_NAME]
    multilabel = settings.get(CommonSettingsLiterals.MULTILABEL, False)
    num_workers = settings[CommonSettingsLiterals.NUM_WORKERS]
    primary_metric = settings[CommonTrainingLiterals.PRIMARY_METRIC]
    training_batch_size = settings[CommonTrainingLiterals.TRAINING_BATCH_SIZE]
    validation_batch_size = settings[CommonTrainingLiterals.VALIDATION_BATCH_SIZE]
    number_of_epochs = settings[CommonTrainingLiterals.NUMBER_OF_EPOCHS]
    enable_onnx_norm = settings[CommonSettingsLiterals.ENABLE_ONNX_NORMALIZATION]
    log_verbose_metrics = settings.get(CommonSettingsLiterals.LOG_VERBOSE_METRICS, False)
    is_enabled_early_stopping = settings[CommonTrainingLiterals.EARLY_STOPPING]
    early_stopping_patience = settings[CommonTrainingLiterals.EARLY_STOPPING_PATIENCE]
    early_stopping_delay = settings[CommonTrainingLiterals.EARLY_STOPPING_DELAY]
    eval_freq = settings[CommonTrainingLiterals.EVALUATION_FREQUENCY]

    distributed = distributed_utils.dist_available_and_initialized()
    master_process = distributed_utils.master_process()
    rank = distributed_utils.get_rank()

    # TODO RK: remove resume for now
    # support resume to handle missing classes
    # TODO: Fix in case of distributed training.
    resume_pkl_file = settings.get(CommonSettingsLiterals.RESUME, None)
    if resume_pkl_file:
        with open(resume_pkl_file, "rb") as fp:
            resume_pkl_model = pickle.load(fp)
        dataset_wrapper.reset_labels(resume_pkl_model.labels)

    model_wrapper = ModelFactory().get_model_wrapper(model_name,
                                                     num_classes=dataset_wrapper.num_classes,
                                                     multilabel=multilabel,
                                                     distributed=distributed,
                                                     rank=rank,
                                                     device=device)

    num_params = sum([p.data.nelement() for p in model_wrapper.model.parameters()])
    logger.info("[model: {}, #param: {}]".format(model_wrapper.model_name, num_params))

    metrics = ClassificationMetrics(num_classes=dataset_wrapper.num_classes, multilabel=multilabel,
                                    detailed=settings[TrainingLiterals.DETAILED_METRICS])

    # setup optimizer
    optimizer = setup_optimizer(model_wrapper.model, settings=settings)

    # check imbalance rate to enable weighted loss to mitigate class imbalance problem
    weighted_loss_factor = settings[TrainingLiterals.WEIGHTED_LOSS]
    imbalance_rate, class_weights = _compute_class_weight(dataset_wrapper, weighted_loss_factor, device=device)
    mesg = "[Input Data] class imbalance rate: {0}, weighted_loss factor: {1}"\
        .format(imbalance_rate, weighted_loss_factor)

    if (weighted_loss_factor == 1 or weighted_loss_factor == 2) and \
            imbalance_rate > settings[TrainingLiterals.IMBALANCE_RATE_THRESHOLD]:
        criterion = _get_criterion(multilabel=multilabel, class_weights=class_weights)
        mesg += ", Weighted loss is applied."
    else:
        criterion = _get_criterion(multilabel=multilabel)
        mesg += ", Weighted loss is NOT applied."
    logger.info(mesg)

    # support resume to load previously trained weights
    # TODO: Fix in case of distributed training.
    if resume_pkl_file:
        model_wrapper.model.load_state_dict(resume_pkl_model.model_wrapper.model.state_dict())
        optimizer.load_state_dict(resume_pkl_model.model_wrapper.optimizer.state_dict())

    best_model_wts = copy.deepcopy(model_wrapper.state_dict())
    best_metric = 0

    # setup dataloader
    train_dataloader, valid_dataloader = _get_train_test_dataloaders(dataset_wrapper, valid_dataset=valid_dataset,
                                                                     resize_to_size=model_wrapper.resize_to_size,
                                                                     crop_size=model_wrapper.crop_size,
                                                                     train_transforms=train_transforms,
                                                                     valid_transforms=valid_transforms,
                                                                     batch_size=training_batch_size,
                                                                     validation_batch_size=validation_batch_size,
                                                                     num_workers=num_workers,
                                                                     distributed=distributed)

    logger.info("[start training: "
                "train batch_size: {}, val batch_size: {}]".format(training_batch_size, validation_batch_size))

    # setup lr_scheduler
    lr_scheduler = setup_lr_scheduler(optimizer, batches_per_epoch=len(train_dataloader), settings=settings)

    # TODO: Fix in case of distributed training.
    if resume_pkl_file:
        lr_scheduler.lr_scheduler.load_state_dict(
            resume_pkl_model.model_wrapper.lr_scheduler.lr_scheduler.state_dict())

    primary_metric_supported = metrics.metric_supported(primary_metric)
    backup_primary_metric = MetricsLiterals.ACCURACY  # Accuracy is always supported.
    if not primary_metric_supported:
        logger.warning("Given primary metric {} is not supported. "
                       "Reporting {} values as {} values.".format(primary_metric,
                                                                  backup_primary_metric, primary_metric))

    no_progress_counter = 0
    epoch_time = AverageMeter()
    epoch_end = time.time()
    train_start = time.time()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()
    model_specs = {
        'multilabel': model_wrapper.multilabel,
        'labels': dataset_wrapper.labels
    }
    for epoch in range(number_of_epochs):

        if distributed:
            if train_dataloader.distributed_sampler is None:
                msg = "train_dataloader.distributed_sampler is None in distributed mode. " \
                      "Cannot shuffle data after each epoch."
                logger.error(msg)
                raise AutoMLVisionSystemException(msg, has_pii=False)
            train_dataloader.distributed_sampler.set_epoch(epoch)

        _train(model_wrapper, epoch=epoch, dataloader=train_dataloader, criterion=criterion, optimizer=optimizer,
               device=device, multilabel=multilabel, system_meter=train_sys_meter, distributed=distributed,
               lr_scheduler=lr_scheduler)

        # save_checkpoints to be added as a runner param when exposed
        if save_checkpoints and master_process:
            save_model_checkpoint(epoch=epoch,
                                  model_name=model_name,
                                  number_of_classes=model_wrapper.number_of_classes,
                                  specs=model_specs,
                                  model_state=model_wrapper.state_dict(),
                                  optimizer_state=optimizer.state_dict(),
                                  lr_scheduler_state=lr_scheduler.lr_scheduler.state_dict(),
                                  output_dir=output_dir,
                                  model_file_name_prefix=str(epoch) + '_')

        final_epoch = epoch + 1 == number_of_epochs
        if epoch % eval_freq == 0 or final_epoch:
            metrics.reset()
            _validate(model_wrapper, dataloader=valid_dataloader, metrics=metrics, device=device,
                      multilabel=multilabel, system_meter=valid_sys_meter, distributed=distributed)

            computed_metrics = metrics.compute()
            if not primary_metric_supported:
                computed_metrics.update({
                    primary_metric: computed_metrics[backup_primary_metric]
                })

            if epoch >= early_stopping_delay:
                # Start incrementing no progress counter only after early_stop_delay_iterations.
                no_progress_counter += 1

            if computed_metrics[primary_metric] >= best_metric and master_process:
                best_model_wts = copy.deepcopy(model_wrapper.state_dict())
                save_model_checkpoint(epoch=epoch,
                                      model_name=model_name,
                                      number_of_classes=model_wrapper.number_of_classes,
                                      specs=model_specs,
                                      model_state=model_wrapper.state_dict(),
                                      optimizer_state=optimizer.state_dict(),
                                      lr_scheduler_state=lr_scheduler.lr_scheduler.state_dict(),
                                      output_dir=output_dir)

            if computed_metrics[primary_metric] > best_metric:
                best_metric = computed_metrics[primary_metric]
                no_progress_counter = 0

            logger.info("Current best metric {0:.3f}".format(best_metric))

        # log to Run History every epoch with previously computed metrics, if not computed in the current epoch
        # to sync the metrics reported index with actual training epoch.
        if master_process and azureml_run is not None:
            utils.log_all_metrics(computed_metrics, azureml_run=azureml_run, add_to_logger=True)

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} " \
               "(avg {epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        if is_enabled_early_stopping and no_progress_counter >= early_stopping_patience:
            logger.info("No progress registered after {0} epochs. "
                        "Early stopping the run.".format(no_progress_counter))
            break

    # measure total training time
    train_time = time.time() - train_start
    utils.log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if master_process:
        logger.info("Writing scoring and featurization scripts.")
        write_scoring_script(output_dir)

        write_artifacts(model_wrapper=model_wrapper,
                        best_model_weights=best_model_wts,
                        labels=dataset_wrapper.labels,
                        output_dir=output_dir,
                        run=azureml_run,
                        best_metric=best_metric,
                        task_type=task_type,
                        device=device,
                        enable_onnx_norm=enable_onnx_norm)

    if log_verbose_metrics:
        utils.log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)


def _get_train_test_dataloaders(
        dataset,
        valid_dataset,
        resize_to_size=None,
        crop_size=None,
        train_transforms=None,
        valid_transforms=None,
        batch_size=None,
        validation_batch_size=None,
        num_workers=None,
        distributed=False):
    if train_transforms is None:
        train_transforms = _get_common_train_transforms(crop_size)

    if valid_transforms is None:
        valid_transforms = _get_common_valid_transforms(resize_to=resize_to_size, crop_size=crop_size)

    train_dataloader = _get_data_loader(dataset, is_train=True, transform_fn=train_transforms,
                                        batch_size=batch_size, num_workers=num_workers, distributed=distributed)
    valid_dataloader = _get_data_loader(valid_dataset, transform_fn=valid_transforms,
                                        batch_size=validation_batch_size,
                                        num_workers=num_workers, distributed=distributed)

    return train_dataloader, valid_dataloader


def _train(model_wrapper, epoch, dataloader=None,
           criterion=None, optimizer=None, device=None, multilabel=False,
           system_meter=None, distributed=False, lr_scheduler=None):

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    model_wrapper.model.train()

    end = time.time()
    uneven_batches_context_manager = model_wrapper.model.join() if \
        distributed_utils.dist_available_and_initialized() else nullcontext()

    with uneven_batches_context_manager:
        for i, (inputs, labels) in enumerate(utils._data_exception_safe_iterator(iter(dataloader))):
            # measure data loading time
            data_time.update(time.time() - end)

            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model_wrapper.model(inputs)
            loss = criterion(outputs, labels)
            loss_value = loss.item()
            # raise an UserException if loss is too big
            utils.check_loss_explosion(loss_value)

            optimizer.zero_grad()
            loss.backward()

            # grad clipping to prevent grad exploding
            torch.nn.utils.clip_grad_value_(model_wrapper.model.parameters(),
                                            clip_value=TrainingCommonSettings.GRADIENT_CLIP_VALUE)
            optimizer.step()

            if lr_scheduler.update_type == LRSchedulerUpdateType.BATCH:
                lr_scheduler.lr_scheduler.step()

            if not multilabel:
                # record loss and measure elapsed time
                prec1 = utils._accuracy(outputs.data, labels)
                top1.update(prec1[0][0], inputs.size(0))
            losses.update(loss_value, inputs.size(0))

            batch_time.update(time.time() - end)
            end = time.time()

            # delete tensors which have a valid grad_fn
            del loss, outputs

            last_batch = i == len(dataloader) - 1
            if i % 100 == 0 or last_batch:
                msg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                      "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                      "({loss.avg:.4f})\t".format(epoch, i, len(dataloader), optimizer.param_groups[0]["lr"],
                                                  batch_time=batch_time, data_time=data_time, loss=losses)
                if not multilabel:
                    msg += "Acc@1 {top1.value:.3f} ({top1.avg:.3f})\t".format(top1=top1)

                msg += system_meter.get_gpu_stats()
                logger.info(msg)
                system_meter.log_system_stats(True)

    if lr_scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        lr_scheduler.lr_scheduler.step()


def _update_metrics(metrics, outputs, labels, model_wrapper):
    probs = model_wrapper.predict_probs_from_outputs(outputs)
    preds = model_wrapper.predict_from_outputs(outputs)
    metrics.update(probs=probs, preds=preds, labels=labels)


def _validate(model_wrapper, dataloader=None, metrics=None, device=None, multilabel=False, system_meter=None,
              distributed=False):
    batch_time = AverageMeter()
    top1 = AverageMeter()

    model_wrapper.model.eval()

    total_outputs_list = []
    total_labels_list = []

    end = time.time()
    with torch.no_grad():
        for i, (inputs, labels) in enumerate(utils._data_exception_safe_iterator(iter(dataloader))):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model_wrapper.model(inputs)
            _update_metrics(metrics, outputs, labels, model_wrapper)

            total_outputs_list.append(outputs)
            total_labels_list.append(labels)

            if not multilabel:
                prec1 = utils._accuracy(outputs.data, labels)
                top1.update(prec1[0][0], inputs.size(0))

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % 100 == 0 or i == len(dataloader) - 1:
                mesg = "Test: [{0}/{1}]\t"\
                       "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, len(dataloader),
                                                                                     batch_time=batch_time)
                if not multilabel:
                    mesg += "Acc@1 {top1.value:.3f} ({top1.avg:.3f})\t".format(top1=top1)
                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(True)

    if not total_labels_list:
        exception_message = "All images in the validation set processed by worker {} are invalid. " \
                            "Cannot compute primary metric.".format(distributed_utils.get_rank())
        raise AutoMLVisionDataException(exception_message, has_pii=False)

    if distributed:
        # Gather metrics data from other workers.
        outputs_list = distributed_utils.all_gather_uneven_tensors(torch.cat(total_outputs_list))
        labels_list = distributed_utils.all_gather_uneven_tensors(torch.cat(total_labels_list))
        if len(outputs_list) != len(labels_list):
            raise AutoMLVisionSystemException("Outputs list is of size {} and labels list is of size {}. "
                                              "Both lists should be of same size after all_gather."
                                              .format(len(outputs_list), len(labels_list)), has_pii=False)

        for index, outputs in enumerate(outputs_list):
            if index != distributed_utils.get_rank():
                _update_metrics(metrics, outputs, labels_list[index], model_wrapper)

    return metrics


def _compute_class_weight(dataset_wrapper, sqrt_pow, device=None):
    """Calculate imbalance rate and class weights for weighted loss to mitigate class imbalance problem

    :param dataset_wrapper: dataset wrapper
    :type dataset_wrapper: azureml.contrib.automl.dnn.vision.io.read.dataset_wrapper.BaseDatasetWrapper
    :param sqrt_pow: square root power when calculating class_weights
    :type sqrt_pow: int
    :param device: device where model should be run (usually "cpu" or "cuda:0" if it is the first gpu)
    :type device: str
    :return: class imbalance ratio and class-level rescaling weights for loss function
    :rtype: Tuple[int, torch.Tensor]
    """

    label_freq_dict = dataset_wrapper.label_freq_dict
    label_freq_list = [0] * dataset_wrapper.num_classes
    for key, val in label_freq_dict.items():
        label_idx = dataset_wrapper.label_to_index_map[key]
        label_freq_list[label_idx] = val

    weights = torch.FloatTensor(label_freq_list).to(device)
    if dataset_wrapper.multilabel:
        # weights in this case are pos_weights
        # pos_weight > 1 increases the recall, pos_weight < 1 increases the precision
        neg_weights = len(dataset_wrapper) - weights
        class_weights = neg_weights / weights
    else:
        class_weights = 1. / weights

    class_weights[class_weights == float("Inf")] = 0
    # sqrt_pow of 2 gives larger variance in class weights than sqrt_pow of 1 in class_weights.
    # In general, class weighting tends to give higher per-class metric but with lower per-instance metrics
    class_weights = torch.sqrt(class_weights) ** sqrt_pow
    logger.info("[class_weights: {}]".format(class_weights))

    imbalance_rate = max(label_freq_list) // max(1, min(label_freq_list))
    return imbalance_rate, class_weights
