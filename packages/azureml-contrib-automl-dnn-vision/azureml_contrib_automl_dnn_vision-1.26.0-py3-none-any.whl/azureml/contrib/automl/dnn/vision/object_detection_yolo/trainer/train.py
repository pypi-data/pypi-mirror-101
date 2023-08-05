# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Contain functions for training and validation """

import copy
import math
import os
import random
import time
import torch

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.artifacts_utils import save_model_checkpoint, write_artifacts
from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.common.constants import TrainingCommonSettings, \
    SettingsLiterals as CommonSettingsLiterals, TrainingLiterals as CommonTrainingLiterals
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter
from azureml.contrib.automl.dnn.vision.common.trainer.lrschedule import LRSchedulerUpdateType
from azureml.contrib.automl.dnn.vision.object_detection.writers.score_script_utils import write_scoring_script
from azureml.contrib.automl.dnn.vision.object_detection_yolo.common.constants import YoloLiterals
from azureml.contrib.automl.dnn.vision.object_detection_yolo.eval.mean_ap import MeanAP
from azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.ema import ModelEMA
from azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.utils import compute_loss, non_max_suppression

logger = get_logger(__name__)


def train_one_epoch(model, ema, optimizer, scheduler, train_loader,
                    epoch, device, system_meter, print_freq=100, tb_writer=None):
    """Train a model for one epoch

    :param model: Model to train
    :type model: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo.Model'>
    :param ema: Model Exponential Moving Average
    :type ema: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.torch_utils.ModelEMA'>
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_loader: Data loader for training data
    :type train_loader: Pytorch data loader
    :param epoch: Current training epoch
    :type epoch: int
    :param device: Target device
    :type device: Pytorch device
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param tb_writer: Tensorboard writer
    :type tb_writer: <class 'torch.utils.tensorboard.writer.SummaryWriter'>
    :returns: mean losses for tensorboard writer
    :rtype: <class 'torch.Tensor'>
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    nb = len(train_loader)
    mloss = torch.zeros(4, device=device)  # mean losses (lbox, lobj, lcls, loss)

    model.train()

    end = time.time()
    for i, (imgs, targets, _) in enumerate(utils._data_exception_safe_iterator(iter(train_loader))):
        # measure data loading time
        data_time.update(time.time() - end)

        ni = i + nb * epoch  # number integrated batches (since train start)
        imgs = imgs.to(device).float() / 255.0  # uint8 to float32, 0 - 255 to 0.0 - 1.0

        # Multi scale : need more CUDA memory for bigger image size
        if model.hyp['multi_scale']:
            imgsz = model.hyp['img_size']
            gs = model.hyp['gs']
            sz = random.randrange(imgsz * 0.5, imgsz * 1.5 + gs) // gs * gs
            sf = sz / max(imgs.shape[2:])
            if sf != 1:
                ns = [math.ceil(x * sf / gs) * gs for x in imgs.shape[2:]]  # new shape (stretched to gs-multiple)
                imgs = torch.nn.functional.interpolate(imgs, size=ns, mode='bilinear', align_corners=False)

        # Forward
        pred = model(imgs)

        # Loss
        loss, loss_items = compute_loss(pred, targets.to(device), model)
        # raise an UserException if loss is too big
        utils.check_loss_explosion(loss.item())
        optimizer.zero_grad()
        loss.backward()

        # grad clipping to prevent grad exploding
        torch.nn.utils.clip_grad_value_(model.parameters(),
                                        clip_value=TrainingCommonSettings.GRADIENT_CLIP_VALUE)
        optimizer.step()
        ema.update(model)

        if scheduler.update_type == LRSchedulerUpdateType.BATCH:
            scheduler.lr_scheduler.step()

        # Tensorboard
        if tb_writer:
            tb_writer.add_scalar('lr', scheduler.lr_scheduler.get_last_lr()[0], ni)

        # record loss and measure elapsed time
        losses.update(loss.item(), len(imgs))
        mloss = (mloss * i + loss_items) / (i + 1)  # update mean losses
        batch_time.update(time.time() - end)
        end = time.time()

        # delete tensors which have a valid grad_fn
        del loss, pred

        if i % print_freq == 0 or i == nb - 1:
            mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3:.5f}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t" \
                   "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                   "({loss.avg:.4f})\t".format(epoch, i, nb, optimizer.param_groups[0]["lr"],
                                               batch_time=batch_time, data_time=data_time, loss=losses)

            mesg += system_meter.get_gpu_stats()
            logger.info(mesg)
            system_meter.log_system_stats(True)

    if scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        scheduler.lr_scheduler.step()

    return mloss


def validate(model, number_of_classes, validation_loader, device, system_meter, conf_thres, iou_thres, print_freq=100):
    """Gets model results on validation set.

    :param model: Model to score
    :type model: Pytorch nn.Module
    :param number_of_classes: number of classes
    :type number_of_classes: int
    :param validation_loader: Data loader for validation data
    :type validation_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter
    :param conf_thres: Confidence threshold
    :type conf_thres: float
    :param iou_thres: IOU threshold
    :type iou_thres: float
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :return: metric scores
    :rtype: tuple of (mean Precision, mean Recall, mean AP@0.5, mean AP@0.5:0.95)
    and <class 'numpy.ndarray'> of (per-class AP@0.5:0.95)
    """

    batch_time = AverageMeter()

    nc = number_of_classes
    nb = len(validation_loader)
    mAP = MeanAP(device, nc=nc, nb=nb)

    model.eval()

    end = time.time()
    for i, (imgs, targets, _) in enumerate(utils._data_exception_safe_iterator(iter(validation_loader))):
        imgs = imgs.to(device).float() / 255.0
        targets = targets.to(device)

        with torch.no_grad():
            # inference and training outputs
            inf_out, _ = model(imgs)

            # TODO: expose multi_label as arg to enable multi labels per box
            # Run NMS
            output = non_max_suppression(inf_out, conf_thres, iou_thres, multi_label=False)

        # TODO: use val_vocmap like faster-rcnn or vice versa?
        mAP.compute_stats(imgs.shape, output, targets)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0 or i == nb - 1:
            mesg = "Test: [{0}/{1}]\t" \
                   "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, nb,
                                                                                 batch_time=batch_time)
            mesg += system_meter.get_gpu_stats()
            logger.info(mesg)
            system_meter.log_system_stats(True)

    return mAP.get_scores()


def train(model_wrapper, optimizer, scheduler, train_loader, validation_loader,
          output_dir=None, azureml_run=None, tb_writer=None, scoring_settings_for_export=None, save_checkpoints=False):
    """Train a model

    :param model_wrapper: Model to train
    :type model_wrapper: BaseObjectDetectionModelWrapper
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_loader: Data loader with training data
    :type train_loader: Pytorch data loader
    :param validation_loader: Data loader with validation data
    :type validation_loader: Pytorch data loader
    :param output_dir: Output directory to write checkpoints to
    :type output_dir: str
     :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run.Run
    :param tb_writer: Tensorboard writer
    :type tb_writer: <class 'torch.utils.tensorboard.writer.SummaryWriter'>
    :param scoring_settings_for_export: Settings for the model
    :type scoring_settings_for_export: dict
    :param save_checkpoints: If True, the checkpoints from each epoch are saved. If False, only the best one.
    :type save_checkpoints: bool
    """

    epoch_time = AverageMeter()

    # Extract relevant parameters from training settings
    settings = model_wrapper.specs
    task_type = settings[CommonSettingsLiterals.TASK_TYPE]
    primary_metric = settings[CommonTrainingLiterals.PRIMARY_METRIC]
    number_of_epochs = settings[CommonTrainingLiterals.NUMBER_OF_EPOCHS]
    enable_onnx_norm = settings[CommonSettingsLiterals.ENABLE_ONNX_NORMALIZATION]
    log_verbose_metrics = settings.get(CommonSettingsLiterals.LOG_VERBOSE_METRICS, False)
    is_enabled_early_stopping = settings[CommonTrainingLiterals.EARLY_STOPPING]
    early_stopping_patience = settings[CommonTrainingLiterals.EARLY_STOPPING_PATIENCE]
    early_stopping_delay = settings[CommonTrainingLiterals.EARLY_STOPPING_DELAY]
    eval_freq = settings[CommonTrainingLiterals.EVALUATION_FREQUENCY]
    conf_thres = settings[YoloLiterals.BOX_SCORE_THRESH]
    iou_thres = settings[YoloLiterals.BOX_IOU_THRESH]

    model = model_wrapper.model
    # Exponential moving average
    ema = ModelEMA(model)

    base_model = model
    device = model_wrapper.device

    best_score = 0.0
    best_model = copy.deepcopy(ema.ema.state_dict())

    no_progress_counter = 0
    computed_metrics = {}

    epoch_end = time.time()
    train_start = time.time()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()
    specs = {
        'model_specs': model_wrapper.specs,
        'classes': model_wrapper.classes
    }
    for epoch in range(number_of_epochs):

        mloss = train_one_epoch(base_model, ema, optimizer, scheduler, train_loader, epoch, device,
                                system_meter=train_sys_meter, tb_writer=tb_writer)

        ema.update_attr(model)

        if save_checkpoints:
            save_model_checkpoint(epoch=epoch,
                                  model_name=model_wrapper.model_name,
                                  number_of_classes=model_wrapper.number_of_classes,
                                  specs=specs,
                                  model_state=ema.ema.state_dict(),
                                  optimizer_state=optimizer.state_dict(),
                                  lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                  output_dir=output_dir,
                                  model_file_name_prefix=str(epoch) + '_')

        final_epoch = epoch + 1 == number_of_epochs
        if epoch % eval_freq == 0 or final_epoch:
            # results for P, R, AP@0.5, AP@0.5:0.95 and maps for per-class AP
            results, maps = validate(ema.ema, len(model_wrapper.classes), validation_loader,
                                     device, valid_sys_meter, conf_thres, iou_thres)

            map_score = results[2]  # AP@0.5
            computed_metrics[primary_metric] = round(map_score, 3)

            # update early stopping counter
            if epoch >= early_stopping_delay:
                no_progress_counter += 1

            if map_score >= best_score:
                save_model_checkpoint(epoch=epoch,
                                      model_name=model_wrapper.model_name,
                                      number_of_classes=model_wrapper.number_of_classes,
                                      specs=specs,
                                      model_state=ema.ema.state_dict(),
                                      optimizer_state=optimizer.state_dict(),
                                      lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                      output_dir=output_dir)
                best_model = copy.deepcopy(ema.ema.state_dict())

            if map_score > best_score:
                best_score = map_score
                no_progress_counter = 0

        # log to Run History every epoch with previously computed metrics, if not computed in the current epoch
        # to sync the metrics reported index with actual training epoch.
        if azureml_run is not None:
            utils.log_all_metrics(computed_metrics, azureml_run=azureml_run, add_to_logger=True)

        # Tensorboard
        if tb_writer:
            tags = ['train/giou_loss', 'train/obj_loss', 'train/cls_loss',
                    'metrics/precision', 'metrics/recall', 'metrics/mAP_0.5', 'metrics/mAP']
            for x, tag in zip(list(mloss[:-1]) + list(results), tags):
                tb_writer.add_scalar(tag, x, epoch)

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        if is_enabled_early_stopping and no_progress_counter > early_stopping_patience:
            logger.info("No progress registered after {0} epochs. "
                        "Early stopping the run.".format(no_progress_counter))
            break

    # measure total training time
    train_time = time.time() - train_start
    utils.log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if log_verbose_metrics:
        utils.log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)

    logger.info("[MAP@0.5] BEST score: {}".format(round(best_score, 3)))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    score_script_dir = os.path.join(os.path.dirname(current_dir), 'writers')
    write_scoring_script(output_dir=output_dir,
                         score_script_dir=score_script_dir,
                         task_type=task_type)

    # this is to make sure the layers in ema can be loaded in the model wrapper
    # without it, the names are different (i.e. "model.0.conv.conv.weight" vs "0.conv.conv.weight")
    best_model_weights = {'model.' + k: v for k, v in best_model.items()}

    write_artifacts(model_wrapper=model_wrapper,
                    best_model_weights=best_model_weights,
                    labels=model_wrapper.classes,
                    output_dir=output_dir,
                    run=azureml_run,
                    best_metric=best_score,
                    task_type=task_type,
                    device=device,
                    enable_onnx_norm=enable_onnx_norm,
                    model_settings=scoring_settings_for_export,
                    is_yolo=True)
