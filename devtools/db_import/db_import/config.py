## Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pathlib
import yaml
import contextlib
import os

from typing import TextIO

PIPELINES_KEY: str = "pipelines"


@contextlib.contextmanager
def _current_working_directory(path: pathlib.Path):
  previous_cwd = pathlib.Path().absolute()

  try:
    os.chdir(path)
    yield path
  finally:
    os.chdir(previous_cwd)


def _embed(loader: yaml.Loader, node):
  """This tag handler allows loading the contents of file as string into a node.

    The initial node's content is interpreted as a file path.
    Relative file path are expected to be relative to the YAML file's location.
    Absolute paths are also allowed but must refer to a location below the YAML
    file's parent directory.

    Example:
    ```yaml
    ---
    property: !embed filename.txt
    """
  yaml_filepath = pathlib.Path(loader.name).resolve()

  with _current_working_directory(yaml_filepath.parent):
    filepath = pathlib.Path(loader.construct_scalar(node)).resolve()
    allowed_directory = yaml_filepath.parent.resolve()
    # We use os.path here to check whether filepath is below allowed_directory,
    # because the equivalent function in pathlib is not available before Python 3.9.
    assert os.path.commonpath([allowed_directory]) == os.path.commonpath(
        [allowed_directory, filepath])
    assert filepath.is_file()
    return filepath.read_text()


yaml.SafeLoader.add_constructor("!embed", _embed)


def load_config(file: TextIO):
  return yaml.safe_load(file)
