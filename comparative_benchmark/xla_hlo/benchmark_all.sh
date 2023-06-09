#!/bin/bash
#
# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set -xeuo pipefail

VENV_DIR="${OOBI_VENV_DIR:-xla-hlo-benchmarks.venv}"
PYTHON="${PYTHON:-/usr/bin/python3}"
XLA_TOOLS_DIR="${OOBI_XLA_TOOLS_DIR:-xla-tools-dir}"
TARGET_DEVICE="${1:-"${OOBI_TARGET_DEVICE}"}"
OUTPUT_PATH="${2:-"${OOBI_OUTPUT}"}"

TD="$(cd $(dirname $0) && pwd)"

VENV_DIR="${VENV_DIR}" PYTHON="${PYTHON}" source "${TD}/setup_venv.sh"

declare -a GPU_BENCHMARK_NAMES=(
  "models/RESNET50_FP32_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/RESNET50_FP16_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/RESNET50_BF16_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/BERT_LARGE_FP32_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/BERT_LARGE_FP16_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/BERT_LARGE_BF16_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/T5_LARGE_FP32_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/T5_LARGE_FP16_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/T5_LARGE_BF16_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/T5_4CG_LARGE_FP32_JAX_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/RESNET50_FP32_TF_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/BERT_LARGE_FP32_TF_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
  "models/T5_LARGE_FP32_TF_.+/inputs/.+/expected_outputs/.+/target_devices/a2-highgpu-1g"
)

declare -a CPU_BENCHMARK_NAMES=(
  "models/RESNET50_FP32_JAX_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/RESNET50_FP32_JAX_.+_BATCH64/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/RESNET50_FP32_JAX_.+_BATCH128/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/BERT_LARGE_FP32_JAX_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/BERT_LARGE_FP32_JAX_.+_BATCH32/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/BERT_LARGE_FP32_JAX_.+_BATCH64/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_LARGE_FP32_JAX_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_LARGE_FP32_JAX_.+_BATCH16/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_LARGE_FP32_JAX_.+_BATCH32/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_4CG_LARGE_FP32_JAX_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_4CG_LARGE_FP32_JAX_.+_BATCH16/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_4CG_LARGE_FP32_JAX_.+_BATCH32/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/RESNET50_FP32_TF_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/RESNET50_FP32_TF_.+_BATCH64/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/RESNET50_FP32_TF_.+_BATCH128/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/BERT_LARGE_FP32_TF_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/BERT_LARGE_FP32_TF_.+_BATCH32/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/BERT_LARGE_FP32_TF_.+_BATCH64/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_LARGE_FP32_TF_.+_BATCH1/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_LARGE_FP32_TF_.+_BATCH16/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
  "models/T5_LARGE_FP32_TF_.+_BATCH32/inputs/.+/expected_outputs/.+/target_devices/c2-standard-16"
)

if [ "${TARGET_DEVICE}" = "a2-highgpu-1g" ]; then
  BENCHMARK_NAMES=("${GPU_BENCHMARK_NAMES[@]}")
  HLO_TOOL="hlo_runner_main"
  ITERATIONS=50
elif [ "${TARGET_DEVICE}" = "c2-standard-16" ]; then
  # Since each iteration includes both compilation and inference, we keep the
  # total iterations small because of the amount of time it takes to do both.
  # Std deviation is <1ms.
  BENCHMARK_NAMES=("${CPU_BENCHMARK_NAMES[@]}")
  HLO_TOOL="run_hlo_module"
  ITERATIONS=5
else
  echo "Unsupported target device ${TARGET_DEVICE}."
  exit 1
fi

"${TD}/../scripts/create_results_json.sh" "${OUTPUT_PATH}"

for benchmark_name in "${BENCHMARK_NAMES[@]}"; do
  "${TD}/run_benchmarks.py" \
    --benchmark_name="${benchmark_name}" \
    --hlo-tool="${XLA_TOOLS_DIR}/${HLO_TOOL}" \
    --output="${OUTPUT_PATH}" \
    --iterations="${ITERATIONS}" \
    --verbose
done
