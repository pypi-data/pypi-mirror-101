# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Model wrappers to build customized Faster RCNN Models."""
import torch
import torchvision

from .base_model_wrapper import BaseObjectDetectionModelWrapper
from ..common.constants import RCNNSpecifications, RCNNBackbones, ModelLiterals
from ...common.pretrained_model_utilities import PretrainedModelFactory
from azureml.automl.core.shared.exceptions import ClientException


def convert_box_score_thresh_to_float_tensor(box_score_thresh_key, **kwargs):
    """If box_score_thresh is present in kwargs, convert it to float32 tensor.

    Inference with onnx model obtained from FasterRCNN model fails in torch 1.7.1 as box_score_thresh
    is interpreted as float64 and float64 is not supported in one of the nodes(Greater).
    Passing it as a torch tensor with float32 type fixes the issue.

    :param box_score_thresh_key: box_score_thresh key
    :type box_score_thresh_key: str
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    :return: modified keyword arguments
    :rtype: dict
    """
    if box_score_thresh_key in kwargs:
        box_score_thresh = kwargs.get(box_score_thresh_key)
        kwargs[box_score_thresh_key] = torch.tensor(box_score_thresh, dtype=torch.float)
    return kwargs


class CustomRCNNSpecifications:
    """Class that contains all specifications necessary to define
    faster rcnn model."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional keyword arguments to define model specifications currently supported:
            -backbone: (string) Key that maps to custom backbone
        :type kwargs: dict
        """

        self._backbone = None

        if "backbone" in kwargs:
            self._backbone = kwargs["backbone"]
        else:
            self._backbone = RCNNSpecifications.DEFAULT_BACKBONE

    @property
    def backbone(self):
        """Get backbone name

        :return: Backbone name
        :rtype: String
        """
        return self._backbone


class CustomRCNNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for custom Faster RCNN Models."""

    _backbone_map = {RCNNBackbones.RESNET_18_FPN_BACKBONE: 'resnet18'}

    def __init__(self, model_name, number_of_classes=None, specs=None, model_settings=None):
        """
        :param model_name: Model name
        :type model_name: str
        :param number_of_classes: Number of object classes
        :type number_of_classes: int
        :param specs: Model specifications
        :type specs: dict
        :param model_settings: Optional argument to define model settings
        :type model_settings: BaseModelSettings
        """
        super().__init__(number_of_classes=number_of_classes, specs=specs, model_name=model_name,
                         model_settings=model_settings)

        self._model = self._create_model(number_of_classes, specs)

    @property
    def model(self):
        """Returns the wrapped model."""
        return self._model

    @model.setter
    def model(self, value):
        """Sets the wrapped model.

        :param value: the model
        :type value: nn.Module
        """
        self._model = value

    def _create_model(self, num_classes, specifications):

        if 'fpn' in specifications.backbone:
            backbone = self._make_backbone(specifications.backbone)
        else:
            backbone = self._make_backbone_no_fpn(specifications.backbone)

        kwargs = {} if self.model_settings is None else self.model_settings.model_init_kwargs()
        kwargs = convert_box_score_thresh_to_float_tensor(ModelLiterals.BOX_SCORE_THRESH, **kwargs)
        model = torchvision.models.detection.faster_rcnn.FasterRCNN(backbone=backbone,
                                                                    num_classes=num_classes, **kwargs)
        return model

    def _make_backbone(self, backbone):

        if backbone in RCNNSpecifications.RESNET_FPN_BACKBONES:
            torch_backbone_name = self._backbone_map[backbone]
            model_backbone = PretrainedModelFactory.resnet_fpn_backbone(
                torch_backbone_name, pretrained=True)
        else:
            raise ClientException('{} not supported'.format(backbone))\
                .with_generic_msg("backbone not supported.")

        return model_backbone

    def _make_backbone_no_fpn(self, backbone):

        if backbone in RCNNSpecifications.CNN_BACKBONES:
            model_backbone = PretrainedModelFactory.mobilenet_v2(pretrained=True).features
            model_backbone.out_channels = 1280
        else:
            raise ClientException('{} not supported'.format(backbone))\
                .with_generic_msg("backbone not supported.")

        return model_backbone
