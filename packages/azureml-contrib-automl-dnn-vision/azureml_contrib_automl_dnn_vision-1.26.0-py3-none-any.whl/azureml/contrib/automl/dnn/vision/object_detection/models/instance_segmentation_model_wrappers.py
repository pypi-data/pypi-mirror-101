# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper function to build instance segmentation wrappers."""
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

from .object_detection_model_wrappers import FasterRCNNResnet50FPNWrapper, FasterRCNNModelSettings
from .object_detection_model_wrappers import ObjectDetectionModelFactory
from ..common.constants import ModelNames, MaskRCNNLiterals, MaskRCNNParameters, ModelLiterals
from .customrcnn import convert_box_score_thresh_to_float_tensor
from ...common.constants import ArtifactLiterals, PretrainedModelNames
from ...common.pretrained_model_utilities import PretrainedModelFactory
from ...common.logging_utils import get_logger

logger = get_logger(__name__)


class MaskRCNNResnet50FPNWrapper(FasterRCNNResnet50FPNWrapper):
    """Model wrapper for Mask RCNN with Resnet50 FPN backbone."""

    def __init__(self, number_of_classes=None, model_state=None, specs=None, model_settings=None):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: int
        :param model_state: Model weights. If None, then a new model is created
        :type model_state: dict
        :param specs: specifications for creating the model
        :type specs: dict
        :param model_settings: Optional argument to define model settings
        :type model_settings: BaseModelSettings
        """
        super().__init__(number_of_classes=number_of_classes, model_state=model_state, specs=specs,
                         model_name=ModelNames.MASK_RCNN_RESNET50_FPN, model_settings=model_settings)

    def _create_model(self, number_of_classes, specs=None, load_pretrained_model_dict=True):
        if specs is None:
            specs = {}

        kwargs = {} if self.model_settings is None else self.model_settings.model_init_kwargs()
        kwargs = convert_box_score_thresh_to_float_tensor(ModelLiterals.BOX_SCORE_THRESH, **kwargs)
        model = PretrainedModelFactory.maskrcnn_resnet50_fpn(pretrained=True,
                                                             load_pretrained_model_dict=load_pretrained_model_dict,
                                                             **kwargs)

        if number_of_classes is not None:
            input_features_box = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(input_features_box,
                                                              number_of_classes)

            input_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
            hidden_layer = specs.get(MaskRCNNLiterals.MASK_PREDICTOR_HIDDEN_DIM,
                                     MaskRCNNParameters.DEFAULT_MASK_PREDICTOR_HIDDEN_DIM)
            model.roi_heads.mask_predictor = MaskRCNNPredictor(input_features_mask,
                                                               hidden_layer,
                                                               number_of_classes)

        return model

    def export_onnx_model(self, file_path=ArtifactLiterals.ONNX_MODEL_FILE_NAME, device=None, enable_norm=False):
        """
        Export the pytorch model to onnx model file.

        :param file_path: file path to save the exported onnx model.
        :type file_path: str
        :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
        :type device: str
        :param enable_norm: enable normalization when exporting onnx
        :type enable_norm: bool
        """
        self._export_onnx_model_with_names(file_path, device, enable_norm,
                                           input_names=['input'],
                                           output_names=['boxes', 'labels', 'scores', 'masks'],
                                           dynamic_axes={'input': {0: 'batch', 1: 'channel', 2: 'height', 3: 'width'},
                                                         'boxes': {0: 'prediction'},
                                                         'labels': {0: 'prediction'},
                                                         'scores': {0: 'prediction'},
                                                         'masks': {0: 'prediction',
                                                                   2: 'height',
                                                                   3: 'width'}})


class InstanceSegmentationModelFactory(ObjectDetectionModelFactory):
    """Factory function to create mask rcnn models."""

    def __init__(self):
        """Init method."""
        super().__init__()

        self._models_dict = {
            ModelNames.MASK_RCNN_RESNET50_FPN: MaskRCNNResnet50FPNWrapper
        }
        self._pre_trained_model_names_dict = {
            ModelNames.MASK_RCNN_RESNET50_FPN: PretrainedModelNames.MASKRCNN_RESNET50_FPN_COCO
        }
        self._model_settings_dict = {
            ModelNames.MASK_RCNN_RESNET50_FPN: FasterRCNNModelSettings
        }
        self._default_model = ModelNames.MASK_RCNN_RESNET50_FPN
