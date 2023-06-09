# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from PIL import Image
import io
import numpy as np
import os
import pathlib
import re
import requests
import shutil
import tarfile

from openxla.benchmark.models import model_interfaces
from typing import Any, Tuple


def download_and_read_img(url: str,
                          width: int = 224,
                          height: int = 224) -> Image.Image:
  """Downloads an image and reads it into memory."""
  data = requests.get(url).content
  img = Image.open(io.BytesIO(data))
  img = img.resize((width, height))
  return img


def generate_and_save_inputs(model_obj: model_interfaces.InferenceModel,
                             model_dir: pathlib.Path) -> Tuple[Any, ...]:
  """Generates and preprocesses inputs, then saves it into `model_dir/input_npy.tz`."""
  # TODO(#44): Support multiple raw inputs.
  raw_inputs = model_obj.generate_default_inputs()
  inputs = model_obj.preprocess(raw_inputs)

  # Save inputs.
  inputs_dir = model_dir.joinpath("inputs")
  inputs_dir.mkdir(exist_ok=True)
  for idx, input in enumerate(inputs):
    input_path = inputs_dir.joinpath(f"input_{idx}.npy")
    np.save(input_path, input)

  with tarfile.open(model_dir.joinpath("inputs_npy.tgz"), "w:gz") as tar:
    tar.add(f"{inputs_dir}/", arcname="")
  shutil.rmtree(inputs_dir)
  return inputs


def save_outputs(outputs: Tuple[Any, ...], model_dir: pathlib.Path) -> None:
  """Saves `outputs` into `model_dir/output_npy.tgz`."""
  outputs_dir = model_dir.joinpath("outputs")
  outputs_dir.mkdir(exist_ok=True)

  for idx, output in enumerate(outputs):
    output_path = outputs_dir.joinpath(f"output_{idx}.npy")
    np.save(output_path, output)

  with tarfile.open(model_dir.joinpath("outputs_npy.tgz"), "w:gz") as tar:
    tar.add(f"{outputs_dir}/", arcname="")
  shutil.rmtree(outputs_dir)


def cleanup_hlo(hlo_dir: pathlib.Path, model_dir: pathlib.Path,
                hlo_filename_regex: str):
  """Takes a HLO dump of files, and renamese and removes relevant files."""
  HLO_STATIC_FILENAME = "xla_hlo_before_optimizations.txt"

  # The filename of the input HLO varies for each model so we rename it to a
  # a known name.
  hlo_files = [
      f for f in os.listdir(hlo_dir) if re.search(hlo_filename_regex, f)
  ]
  if len(hlo_files) != 1:
    raise RuntimeError("Could not find HLO file")

  shutil.move(str(hlo_dir.joinpath(hlo_files[0])),
              str(model_dir.joinpath(HLO_STATIC_FILENAME)))
  shutil.rmtree(hlo_dir)
