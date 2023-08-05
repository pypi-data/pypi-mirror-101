# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""

import argparse
import os
import time

from azureml.core.run import Run
from azureml.automl.core.shared.exceptions import ClientException

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import TrainingLiterals as CommonTrainingLiterals
from azureml.contrib.automl.dnn.vision.object_detection_yolo.writers.score import _score_with_model
from azureml.contrib.automl.dnn.vision.common.constants import (
    ArtifactLiterals, SettingsLiterals, DistributedLiterals
)
from azureml.contrib.automl.dnn.vision.common.trainer.lrschedule import setup_lr_scheduler
from azureml.contrib.automl.dnn.vision.common.trainer.optimize import setup_optimizer

from .common.constants import (
    yolo_hyp_defaults, training_settings_defaults, TrainingLiterals,
    YoloLiterals, YoloParameters
)
from .data.datasets import FileObjectDetectionDatasetWrapperYolo, AmlDatasetObjectDetectionWrapperYolo
from .trainer.train import train
from .utils.utils import check_img_size, init_seeds
from ..common import distributed_utils
from ..common.data_utils import get_labels_files_paths_from_settings, validate_labels_files_paths
from ..common.exceptions import AutoMLVisionValidationException
from ..common.logging_utils import get_logger
from ..common.parameters import add_task_agnostic_train_parameters
from ..common.system_meter import SystemMeter
from ..common.sku_validation import validate_gpu_sku
from ..object_detection.common.constants import ModelNames
from ..object_detection.common.object_detection_utils import score_validation_data
from ..object_detection.data.loaders import setup_dataloader
from ..object_detection.data.utils import read_aml_dataset, read_file_dataset
from ..object_detection.models import detection

azureml_run = Run.get_context()

logger = get_logger(__name__)


def setup_dataloaders(settings, output_directory):
    """Settings for (file and aml) datasets and data loaders

    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    :param output_directory: Name of dir to save files for training/validation dataset
    :type output_directory: String
    :return: train_loader and validation_loader
    :rtype: Tuple of form (dataloaders.RobustDataLoader, dataloaders.RobustDataLoader)
    """
    # Settings for Aml dataset
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    # Settings for both
    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    settings['img_size'] = check_img_size(settings['img_size'], settings['gs'])

    # Setup Dataset
    if utils.is_aml_dataset_input(settings):
        train_dataset, validation_dataset = read_aml_dataset(dataset_id=dataset_id,
                                                             validation_dataset_id=validation_dataset_id,
                                                             settings=settings,
                                                             ignore_data_errors=ignore_data_errors,
                                                             output_dir=output_directory,
                                                             master_process=distributed_utils.master_process(),
                                                             dataset_class=AmlDatasetObjectDetectionWrapperYolo,
                                                             download_files=True,
                                                             use_bg_label=False)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)

        if image_folder is None:
            raise ClientException("images_folder or dataset_id needs to be specified", has_pii=False)
        else:
            image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        train_labels_file, val_labels_file = get_labels_files_paths_from_settings(settings)

        train_dataset, validation_dataset = read_file_dataset(image_folder=image_folder,
                                                              annotations_file=train_labels_file,
                                                              annotations_test_file=val_labels_file,
                                                              settings=settings,
                                                              ignore_data_errors=ignore_data_errors,
                                                              output_dir=output_directory,
                                                              dataset_class=FileObjectDetectionDatasetWrapperYolo,
                                                              master_process=distributed_utils.master_process(),
                                                              use_bg_label=False)
        logger.info("[train file: {}, validation file: {}]".format(train_labels_file, val_labels_file))

    # Update classes
    if train_dataset.classes != validation_dataset.classes:
        all_classes = list(set(train_dataset.classes + validation_dataset.classes))
        train_dataset.reset_classes(all_classes)
        validation_dataset.reset_classes(all_classes)

    logger.info("[# train images: {}, # validation images: {}, # labels: {}, image size: {}]".format(
        len(train_dataset), len(validation_dataset), train_dataset.num_classes, settings['img_size']))

    # Setup Dataloaders
    train_dataloader_settings = {'batch_size': settings[CommonTrainingLiterals.TRAINING_BATCH_SIZE],
                                 'shuffle': True,
                                 'num_workers': settings[SettingsLiterals.NUM_WORKERS]}
    val_dataloader_settings = {'batch_size': settings[CommonTrainingLiterals.VALIDATION_BATCH_SIZE],
                               'shuffle': False,
                               'num_workers': settings[SettingsLiterals.NUM_WORKERS]}

    train_loader = setup_dataloader(train_dataset, **train_dataloader_settings)
    validation_loader = setup_dataloader(validation_dataset, **val_dataloader_settings)

    return train_loader, validation_loader


@utils._exception_handler
def run(automl_settings):
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    """
    script_start_time = time.time()

    settings, unknown = _parse_argument_settings(automl_settings)

    utils._top_initialization(settings)

    task_type = settings.get(SettingsLiterals.TASK_TYPE, None)

    if not task_type:
        raise AutoMLVisionValidationException("Task type was not found in automl settings.",
                                              has_pii=False)
    utils._set_logging_parameters(task_type, settings)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    # TODO: support multi-gpu
    if DistributedLiterals.DISTRIBUTED in settings:
        if settings[DistributedLiterals.DISTRIBUTED]:
            logger.error("Distributed is not supported for yolo. Continuing with a single gpu.")
            settings[DistributedLiterals.DISTRIBUTED] = False
    else:
        settings[DistributedLiterals.DISTRIBUTED] = False

    # TODO JEDI
    # This is ok to log now because it can only be system metadata. When we expose the package to customers
    # we need to revisit.
    logger.info("Final settings: \n {}".format(settings))

    validate_labels_files_paths(settings)

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    tb_writer = utils.init_tensorboard()

    # Set random seed
    init_seeds(1)

    device = settings[SettingsLiterals.DEVICE]
    validate_gpu_sku(device=device)
    output_directory = ArtifactLiterals.OUTPUT_DIR

    utils.warn_for_cpu_devices(device, azureml_run)

    # Set data loaders
    train_loader, validation_loader = setup_dataloaders(settings, output_directory)

    # Update # of class
    nc = train_loader.dataset.num_classes

    # Create model
    settings['cls'] *= nc / 80.  # scale coco-tuned settings['cls'] to current dataset
    settings['gr'] = 1.0  # giou loss ratio (obj_loss = 1.0 or giou)

    model_wrapper = detection.setup_model(model_name=ModelNames.YOLO_V5,
                                          number_of_classes=nc,
                                          classes=train_loader.dataset.classes,
                                          device=device,
                                          distributed=False,
                                          # TODO only add the relevant fields in the settings
                                          specs=settings)
    # TODO: when large or xlarge is chosen, reduce batch_size to avoid CUDA out of memory
    if device != 'cpu' and model_wrapper.model_size in ['large', 'xlarge']:
        logger.warning("[model_size (medium) is supported on 12GiB GPU memory with a batch_size of 16. "
                       "Your choice of model_size ({}) and a batch_size of {} might lead to CUDA OOM]"
                       .format(model_wrapper.model_size, settings[CommonTrainingLiterals.TRAINING_BATCH_SIZE]))

    num_params = sum(x.numel() for x in model_wrapper.parameters())  # number parameters
    logger.info("[model: {} ({}), # layers: {}, # param: {}]".format(settings[SettingsLiterals.MODEL_NAME],
                                                                     model_wrapper.model_size,
                                                                     len(list(model_wrapper.parameters())),
                                                                     num_params))

    # setup optimizer
    optimizer = setup_optimizer(model_wrapper.model, settings=settings)
    # setup lr_scheduler
    lr_scheduler = setup_lr_scheduler(optimizer, batches_per_epoch=len(train_loader), settings=settings)

    # Train
    scoring_settings = {
        YoloLiterals.BOX_SCORE_THRESH: settings[TrainingLiterals.SCORING_BOX_SCORE_THRESH],
        YoloLiterals.BOX_IOU_THRESH: settings[TrainingLiterals.SCORING_BOX_IOU_THRESH]
    }
    train(model_wrapper=model_wrapper, optimizer=optimizer, scheduler=lr_scheduler,
          train_loader=train_loader, validation_loader=validation_loader,
          output_dir=output_directory, azureml_run=azureml_run, tb_writer=tb_writer,
          scoring_settings_for_export=scoring_settings)

    # Run scoring
    run_scoring = settings.get(SettingsLiterals.OUTPUT_SCORING, False)
    if run_scoring:
        score_validation_data(run=azureml_run, model_settings=scoring_settings,
                              settings=settings, device=device,
                              score_with_model=_score_with_model)

    utils.log_script_duration(script_start_time, settings, azureml_run)


def _parse_argument_settings(automl_settings):
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description="Object detection - YoloV5", allow_abbrev=False)
    add_task_agnostic_train_parameters(parser, training_settings_defaults)

    # Yolov5 Settings
    parser.add_argument(utils._make_arg(YoloLiterals.IMG_SIZE), type=int,
                        help='image size for train and val',
                        default=YoloParameters.DEFAULT_IMG_SIZE)
    parser.add_argument(utils._make_arg(YoloLiterals.MODEL_SIZE), type=str,
                        help='model size (small, medium, large, xlarge)',
                        default=YoloParameters.DEFAULT_MODEL_SIZE)
    parser.add_argument(utils._make_arg(YoloLiterals.MULTI_SCALE),
                        help='vary img-size +/- 50%%', action="store_true")

    # inference settings
    parser.add_argument(utils._make_arg(TrainingLiterals.SCORING_BOX_SCORE_THRESH), type=float,
                        help="during inference, only return proposals with a score \
                              greater than box_score_thresh. The score is the multiplication of \
                              the objectness score and classification probability",
                        default=training_settings_defaults[TrainingLiterals.SCORING_BOX_SCORE_THRESH])
    parser.add_argument(utils._make_arg(TrainingLiterals.SCORING_BOX_IOU_THRESH), type=float,
                        help="IOU threshold used during inference in nms post processing",
                        default=training_settings_defaults[TrainingLiterals.SCORING_BOX_IOU_THRESH])

    # Extract Commandline Settings
    args, unknown = parser.parse_known_args()

    args_dict = utils.parse_model_conditional_space(vars(args))

    # Update training default settings with yolo specific hyper-parameters
    training_settings_defaults.update(yolo_hyp_defaults)

    # Training settings
    return utils._merge_settings_args_defaults(automl_settings, args_dict, training_settings_defaults), unknown
