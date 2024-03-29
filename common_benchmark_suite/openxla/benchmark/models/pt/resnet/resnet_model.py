# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from PIL import Image
import torch
import torchvision.models
from typing import Any, Callable

from openxla.benchmark.models import model_interfaces, utils

DEFAULT_IMAGE_URL = "https://storage.googleapis.com/iree-model-artifacts/ILSVRC2012_val_00000023.JPEG"


class ResNet(torch.nn.Module, model_interfaces.InferenceModel):
  """We use the ResNet variant listed in MLPerf here:
  https://github.com/mlcommons/inference/tree/master/vision/classification_and_detection
  Input size 3x224x224 is used, as stated in the MLPerf Inference Rules:
  https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#41-benchmarks
  """

  model: torchvision.models.ResNet
  preprocessor: Callable[[Any], torch.Tensor]
  batch_size: int
  dtype: torch.dtype

  def __init__(self, batch_size: int, dtype: torch.dtype, model_name: str):
    super().__init__()

    if model_name == "torchvision/resnet50":
      weights = torchvision.models.ResNet50_Weights.DEFAULT
      model = torchvision.models.resnet50(weights=weights).to(dtype)
      preprocessor = weights.transforms()
    else:
      raise ValueError(f"Unsupported model: '{model_name}'")

    self.model = model
    self.preprocessor = preprocessor
    self.batch_size = batch_size
    self.dtype = dtype
    self.train(False)

  def generate_default_inputs(self) -> Image.Image:
    # TODO(#44): This should go away once we support different raw inputs.
    return utils.download_and_read_img(DEFAULT_IMAGE_URL)

  def preprocess(self, input_image: Image.Image) -> torch.Tensor:
    resized_image = input_image.resize((224, 224))
    tensor = self.preprocessor(resized_image).to(dtype=self.dtype).unsqueeze(0)
    return tensor.repeat(self.batch_size, 1, 1, 1)

  def forward(self, input: torch.Tensor) -> torch.Tensor:
    return self.model(input)


DTYPE_MAP = {
    "fp32": torch.float32,
    "fp16": torch.float16,
}


def create_model(batch_size: int = 1,
                 data_type: str = "fp32",
                 model_name: str = "torchvision/resnet50",
                 **_unused_params) -> ResNet:
  """Configure and create a PyTorch ResNet model instance.

  Args:
    batch_size: input batch size
    data_type: model data type. Available options: `fp32`, `fp16`
    model_name: The name of the ResNet variant to use. Supported variants
      include: `torchvision/resnet50`
  Returns:
    A PyTorch ResNet model.
  """
  dtype = DTYPE_MAP.get(data_type)
  if dtype is None:
    raise ValueError(f"Unsupported data type: '{data_type}'.")

  return ResNet(batch_size=batch_size, dtype=dtype, model_name=model_name)
