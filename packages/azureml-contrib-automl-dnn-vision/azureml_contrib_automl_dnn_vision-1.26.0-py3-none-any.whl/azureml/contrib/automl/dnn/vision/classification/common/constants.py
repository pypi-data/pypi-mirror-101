# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines literals and constants for the classification part of the package."""

from azureml.contrib.automl.dnn.vision.common.constants import (
    ArtifactLiterals, CommonSettings, DistributedLiterals, DistributedParameters, MetricsLiterals,
    SettingsLiterals as CommonSettingsLiterals, TrainingCommonSettings, TrainingLiterals as CommonTrainingLiterals,
    safe_to_log_vision_common_settings, safe_to_log_automl_settings
)


class PredictionLiterals:
    """Strings that will be keys in the output json during prediction."""
    FEATURE_VECTOR = 'feature_vector'
    FILENAME = 'filename'
    LABELS = 'labels'
    PROBS = 'probs'


class TrainingLiterals:
    """String keys for training parameters."""
    # Report detailed metrics like per class/sample f1, f2, precision, recall scores.
    DETAILED_METRICS = 'detailed_metrics'
    # data imbalance ratio (#data from largest class /#data from smallest class)
    IMBALANCE_RATE_THRESHOLD = "imbalance_rate_threshold"
    PARAMS = 'params'
    TEST_RATIO = 'test_ratio'
    # applying class-level weighting in weighted loss for class imbalance
    WEIGHTED_LOSS = "weighted_loss"


class LoggingLiterals:
    """Literals that help logging and correlating different training runs."""
    PROJECT_ID = 'project_id'
    VERSION_NUMBER = 'version_number'
    TASK_TYPE = 'task_type'


class ModelNames:
    """Currently supported model names."""
    RESNET18 = 'resnet18'
    RESNET50 = 'resnet50'
    MOBILENETV2 = 'mobilenetv2'
    SERESNEXT = 'seresnext'


class PackageInfo:
    """Contains package details."""
    PYTHON_VERSION = '3.6'
    CONDA_PACKAGE_NAMES = ['pip']
    PIP_PACKAGE_NAMES = ['azureml-contrib-automl-dnn-vision']


base_training_settings_defaults = {
    CommonSettingsLiterals.DEVICE: CommonSettings.DEVICE,
    CommonSettingsLiterals.DATA_FOLDER: CommonSettings.DATA_FOLDER,
    CommonSettingsLiterals.LABELS_FILE_ROOT: CommonSettings.LABELS_FILE_ROOT,
    CommonTrainingLiterals.NUMBER_OF_EPOCHS: 15,
    CommonTrainingLiterals.TRAINING_BATCH_SIZE: 78,
    CommonTrainingLiterals.VALIDATION_BATCH_SIZE: 78,
    CommonTrainingLiterals.EARLY_STOPPING: TrainingCommonSettings.DEFAULT_EARLY_STOPPING,
    CommonTrainingLiterals.EARLY_STOPPING_PATIENCE: TrainingCommonSettings.DEFAULT_EARLY_STOPPING_PATIENCE,
    CommonTrainingLiterals.EARLY_STOPPING_DELAY: TrainingCommonSettings.DEFAULT_EARLY_STOPPING_DELAY,
    CommonTrainingLiterals.OPTIMIZER: TrainingCommonSettings.DEFAULT_OPTIMIZER,
    CommonTrainingLiterals.MOMENTUM: TrainingCommonSettings.DEFAULT_MOMENTUM,
    CommonTrainingLiterals.WEIGHT_DECAY: TrainingCommonSettings.DEFAULT_WEIGHT_DECAY,
    CommonTrainingLiterals.NESTEROV: TrainingCommonSettings.DEFAULT_NESTEROV,
    CommonTrainingLiterals.BETA1: TrainingCommonSettings.DEFAULT_BETA1,
    CommonTrainingLiterals.BETA2: TrainingCommonSettings.DEFAULT_BETA2,
    CommonTrainingLiterals.AMSGRAD: TrainingCommonSettings.DEFAULT_AMSGRAD,
    CommonTrainingLiterals.LR_SCHEDULER: TrainingCommonSettings.DEFAULT_LR_SCHEDULER,
    CommonTrainingLiterals.STEP_LR_GAMMA: TrainingCommonSettings.DEFAULT_STEP_LR_GAMMA,
    CommonTrainingLiterals.STEP_LR_STEP_SIZE: TrainingCommonSettings.DEFAULT_STEP_LR_STEP_SIZE,
    CommonTrainingLiterals.WARMUP_COSINE_LR_CYCLES: TrainingCommonSettings.DEFAULT_WARMUP_COSINE_LR_CYCLES,
    CommonTrainingLiterals.WARMUP_COSINE_LR_WARMUP_EPOCHS:
        TrainingCommonSettings.DEFAULT_WARMUP_COSINE_LR_WARMUP_EPOCHS,
    CommonTrainingLiterals.EVALUATION_FREQUENCY: TrainingCommonSettings.DEFAULT_EVALUATION_FREQUENCY,
    CommonSettingsLiterals.ENABLE_ONNX_NORMALIZATION: False,
    CommonSettingsLiterals.IGNORE_DATA_ERRORS: True,
    CommonSettingsLiterals.LOG_SCORING_FILE_INFO: False,
    CommonSettingsLiterals.MULTILABEL: False,
    CommonSettingsLiterals.NUM_WORKERS: 8,
    CommonSettingsLiterals.OUTPUT_DIR: ArtifactLiterals.OUTPUT_DIR,
    CommonSettingsLiterals.OUTPUT_SCORING: False,
    TrainingLiterals.DETAILED_METRICS: True,
    TrainingLiterals.IMBALANCE_RATE_THRESHOLD: 2,
    TrainingLiterals.TEST_RATIO: 0.2,
    TrainingLiterals.WEIGHTED_LOSS: 0,
    DistributedLiterals.DISTRIBUTED: DistributedParameters.DEFAULT_DISTRIBUTED,
    DistributedLiterals.MASTER_ADDR: DistributedParameters.DEFAULT_MASTER_ADDR,
    DistributedLiterals.MASTER_PORT: DistributedParameters.DEFAULT_MASTER_PORT
}

multiclass_training_settings_defaults = {
    CommonTrainingLiterals.PRIMARY_METRIC: MetricsLiterals.ACCURACY,
    CommonTrainingLiterals.LEARNING_RATE: 0.01,
}

multilabel_training_settings_defaults = {
    CommonTrainingLiterals.PRIMARY_METRIC: MetricsLiterals.IOU,
    CommonTrainingLiterals.LEARNING_RATE: 0.035,
}

scoring_settings_defaults = {
    CommonSettingsLiterals.NUM_WORKERS: 8
}

featurization_settings_defaults = {
    CommonSettingsLiterals.NUM_WORKERS: 8
}

safe_to_log_vision_classification_settings = {
    TrainingLiterals.DETAILED_METRICS,
    TrainingLiterals.IMBALANCE_RATE_THRESHOLD,
    TrainingLiterals.PARAMS,
    TrainingLiterals.TEST_RATIO,
    TrainingLiterals.WEIGHTED_LOSS,
}

safe_to_log_settings = \
    safe_to_log_automl_settings | \
    safe_to_log_vision_common_settings | \
    safe_to_log_vision_classification_settings
