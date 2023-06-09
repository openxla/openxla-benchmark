#!/bin/bash
#
# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# Runs `generate_model_artifacts.py` on all registered JAX models and saves
# artifacts into the directory `/tmp/jax_models_<jax-version>_<timestamp>`.
#
# Once complete. please upload the output directory to
# `gs://iree-model-artifacts/jax`, preserving directory name.
#
# Usage:
#     bash generate_saved_models.sh <path_to_iree_opt>
#
# Requires python-3.10 and above and python-venv.
#
# Environment variables:
#   VENV_DIR=jax-models.venv
#   PYTHON=/usr/bin/python3.10
#   WITH_CUDA=1

set -xeuo pipefail

TD="$(cd $(dirname $0) && pwd)"
VENV_DIR="${VENV_DIR:-jax-models.venv}"
PYTHON="${PYTHON:-"$(which python)"}"
WITH_CUDA="${WITH_CUDA:-}"

# See https://openxla.github.io/iree/building-from-source/getting-started/ for
# instructions on how to build `iree-opt`.
IREE_OPT_PATH=$1

VENV_DIR=${VENV_DIR} PYTHON=${PYTHON} WITH_CUDA=${WITH_CUDA} "${TD}/setup_venv.sh"
source ${VENV_DIR}/bin/activate

# Generate unique output directory.
JAX_VERSION=$(pip show jax | grep Version | sed -e "s/^Version: \(.*\)$/\1/g")
DIR_NAME="jax_models_${JAX_VERSION}_$(date +'%s')"
OUTPUT_DIR="/tmp/${DIR_NAME}"
mkdir "${OUTPUT_DIR}"

pip list > "${OUTPUT_DIR}/models_version_info.txt"

python "${TD}/generate_model_artifacts.py" -o "${OUTPUT_DIR}" --iree_opt_path="${IREE_OPT_PATH}"
