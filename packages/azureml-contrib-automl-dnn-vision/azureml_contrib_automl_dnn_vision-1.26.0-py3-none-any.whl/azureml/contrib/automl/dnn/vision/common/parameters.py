# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Parameters that apply to model training/scoring"""
from argparse import ArgumentParser
from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import (
    SettingsLiterals, TrainingLiterals, OptimizerType, LrSchedulerType
)


def add_task_agnostic_train_parameters(parser: ArgumentParser, default_values: dict):
    """Adds to the parser the parameters that are task agnostic.

    :param parser: args parser
    :type parser: ArgumentParser
    :param default_values: default values for the parameters
    :type default_values: dict
    :return: None
    """
    # Model and Device Settings
    utils.add_model_arguments(parser)

    parser.add_argument(utils._make_arg(SettingsLiterals.DEVICE), type=str,
                        help="Device to train on (cpu/cuda:0/cuda:1,...)",
                        default=default_values[SettingsLiterals.DEVICE])

    # Epochs and batch size
    parser.add_argument(utils._make_arg(TrainingLiterals.NUMBER_OF_EPOCHS), type=int,
                        help="Number of training epochs",
                        default=default_values[TrainingLiterals.NUMBER_OF_EPOCHS])

    parser.add_argument(utils._make_arg(TrainingLiterals.TRAINING_BATCH_SIZE), type=int,
                        help="Training batch size",
                        default=default_values[TrainingLiterals.TRAINING_BATCH_SIZE])

    parser.add_argument(utils._make_arg(TrainingLiterals.VALIDATION_BATCH_SIZE), type=int,
                        help="Validation batch size",
                        default=default_values[TrainingLiterals.VALIDATION_BATCH_SIZE])

    # Early termination
    parser.add_argument(utils._make_arg(TrainingLiterals.EARLY_STOPPING), type=bool,
                        help="Enable early stopping logic during training",
                        default=default_values[TrainingLiterals.EARLY_STOPPING])

    parser.add_argument(utils._make_arg(TrainingLiterals.EARLY_STOPPING_PATIENCE), type=int,
                        help="Minimum number of epochs/validation evaluations "
                             "with no primary metric score improvement before the run is stopped",
                        default=default_values[TrainingLiterals.EARLY_STOPPING_PATIENCE])

    parser.add_argument(utils._make_arg(TrainingLiterals.EARLY_STOPPING_DELAY), type=int,
                        help="Minimum number of epochs/validation evaluations "
                             "to wait before primary metric score improvement is tracked for early stopping",
                        default=default_values[TrainingLiterals.EARLY_STOPPING_DELAY])

    # Learning rate and learning rate scheduler
    parser.add_argument(utils._make_arg(TrainingLiterals.LEARNING_RATE), type=float,
                        help="Initial learning rate",
                        default=default_values[TrainingLiterals.LEARNING_RATE])

    parser.add_argument(utils._make_arg(TrainingLiterals.LR_SCHEDULER), type=str,
                        choices=LrSchedulerType.ALL_TYPES,
                        help="Type of learning rate scheduler in {warmup_cosine, step}",
                        default=default_values[TrainingLiterals.LR_SCHEDULER])

    parser.add_argument(utils._make_arg(TrainingLiterals.STEP_LR_GAMMA), type=float,
                        help="Value of gamma for the learning rate scheduler if it is of type step",
                        default=default_values[TrainingLiterals.STEP_LR_GAMMA])

    parser.add_argument(utils._make_arg(TrainingLiterals.STEP_LR_STEP_SIZE), type=int,
                        help="Value of step_size for the learning rate scheduler if it is of type step",
                        default=default_values[TrainingLiterals.STEP_LR_STEP_SIZE])

    parser.add_argument(utils._make_arg(TrainingLiterals.WARMUP_COSINE_LR_CYCLES), type=float,
                        help="Value of cosine cycle for the learning rate scheduler if it is of type warmup_cosine",
                        default=default_values[TrainingLiterals.WARMUP_COSINE_LR_CYCLES])

    parser.add_argument(utils._make_arg(TrainingLiterals.WARMUP_COSINE_LR_WARMUP_EPOCHS), type=int,
                        help="Value of warmup epochs for the learning rate scheduler if it is of type warmup_cosine",
                        default=default_values[TrainingLiterals.WARMUP_COSINE_LR_WARMUP_EPOCHS])

    # Optimizer
    parser.add_argument(utils._make_arg(TrainingLiterals.OPTIMIZER), type=str,
                        default=default_values[TrainingLiterals.OPTIMIZER],
                        choices=OptimizerType.ALL_TYPES,
                        help="Type of optimizer in {sgd, adam, adamw}")

    parser.add_argument(utils._make_arg(TrainingLiterals.MOMENTUM), type=float,
                        default=default_values[TrainingLiterals.MOMENTUM],
                        help="Value of momentum for the optimizer if it is of type sgd")

    parser.add_argument(utils._make_arg(TrainingLiterals.WEIGHT_DECAY), type=float,
                        default=default_values[TrainingLiterals.WEIGHT_DECAY],
                        help="Value of weight_decay for the optimizer if it is of type sgd or adam or adamw")

    parser.add_argument(utils._make_arg(TrainingLiterals.NESTEROV), type=bool,
                        default=default_values[TrainingLiterals.NESTEROV],
                        help="Enable nesterov for the optimizer if it is of type sgd")

    parser.add_argument(utils._make_arg(TrainingLiterals.BETA1), type=float,
                        default=default_values[TrainingLiterals.BETA1],
                        help="Value of beta1 for the optimizer if it is of type adam or adamw")

    parser.add_argument(utils._make_arg(TrainingLiterals.BETA2), type=float,
                        default=default_values[TrainingLiterals.BETA2],
                        help="Value of beta2 for the optimizer if it is of type adam or adamw")

    parser.add_argument(utils._make_arg(TrainingLiterals.AMSGRAD), type=bool,
                        default=default_values[TrainingLiterals.AMSGRAD],
                        help="Enable amsgrad for the optimizer if it is of type adam or adamw")

    # Evaluation
    parser.add_argument(utils._make_arg(TrainingLiterals.EVALUATION_FREQUENCY), type=int,
                        default=default_values[TrainingLiterals.EVALUATION_FREQUENCY],
                        help="Frequency to evaluate validation dataset to get metric scores")

    # Data path for internal use only. Only labeled datasets is allowed for built-in models
    parser.add_argument(utils._make_arg(SettingsLiterals.DATA_FOLDER),
                        utils._make_arg(SettingsLiterals.DATA_FOLDER.replace("_", "-")), type=str,
                        default=default_values[SettingsLiterals.DATA_FOLDER],
                        help="root of the blob store")

    parser.add_argument(utils._make_arg(SettingsLiterals.LABELS_FILE_ROOT),
                        utils._make_arg(SettingsLiterals.LABELS_FILE_ROOT.replace("_", "-")), type=str,
                        default=default_values[SettingsLiterals.LABELS_FILE_ROOT],
                        help="root relative to which label file paths exist")
