# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import itertools
import string

from openxla.benchmark import def_types, unique_ids
from openxla.benchmark.comparative_suite import utils

PARENT_GCS_DIR = "https://storage.googleapis.com/iree-model-artifacts/pytorch/pt_models_20230709.894_1688992116/"

# Bert models.
# Model implementation from https://huggingface.co/docs/transformers/model_doc/bert#transformers.BertModel.
# Batch sizes from MLPerf A100 Configs: https://github.com/mlcommons/inference_results_v2.1/tree/master/closed/NVIDIA/configs/bert
BERT_PT_IMPL = def_types.ModelImplementation(
    id=unique_ids.MODEL_IMPL_BERT_PT,
    name="BERT_PT",
    tags=["transformer-encoder", "bert"],
    framework_type=def_types.ModelFrameworkType.PYTORCH,
    module_path=f"{utils.MODELS_MODULE_PATH}.pt.bert.bert_model",
    source_info=
    "https://huggingface.co/docs/transformers/model_doc/bert#transformers.BertModel",
)

BERT_LARGE_FP32_PT_384XI32_BATCH_TEMPLATE = utils.ModelTemplate(
    id=utils.BATCH_ID(unique_ids.MODEL_BERT_LARGE_FP32_PT_384XI32),
    name=utils.BATCH_NAME("BERT_LARGE_FP32_PT_384XI32"),
    tags=[utils.BATCH_TAG],
    model_impl=BERT_PT_IMPL,
    model_parameters={
        "batch_size": utils.BATCH_SIZE_PARAM,
        "data_type": "fp32",
        "seq_len": 384,
        "model_name": "bert-large-uncased",
        "import_on_gpu": False,
        "import_with_fx": True,
    },
    artifacts={
        def_types.ModelArtifactType.LINALG_MLIR:
            utils.ModelArtifactTemplate(
                artifact_type=def_types.ModelArtifactType.STABLEHLO_MLIR,
                source_url=string.Template(
                    PARENT_GCS_DIR +
                    "BERT_LARGE_FP32_PT_384XI32_BATCH${batch_size}/linalg.mlirbc"
                ),
            ),
    })

BERT_LARGE_FP16_PT_384XI32_BATCH_TEMPLATE = utils.ModelTemplate(
    id=utils.BATCH_ID(unique_ids.MODEL_BERT_LARGE_FP16_PT_384XI32),
    name=utils.BATCH_NAME("BERT_LARGE_FP16_PT_384XI32"),
    tags=[utils.BATCH_TAG],
    model_impl=BERT_PT_IMPL,
    model_parameters={
        "batch_size": utils.BATCH_SIZE_PARAM,
        "data_type": "fp16",
        "seq_len": 384,
        "model_name": "bert-large-uncased",
        "import_on_gpu": True,
        "import_with_fx": True,
    },
    artifacts={
        def_types.ModelArtifactType.LINALG_MLIR:
            utils.ModelArtifactTemplate(
                artifact_type=def_types.ModelArtifactType.STABLEHLO_MLIR,
                source_url=string.Template(
                    PARENT_GCS_DIR +
                    "BERT_LARGE_FP16_PT_384XI32_BATCH${batch_size}/linalg.mlirbc"
                ),
            ),
    })

BERT_LARGE_FP32_PT_384XI32_BATCHES = utils.build_batch_models(
    template=BERT_LARGE_FP32_PT_384XI32_BATCH_TEMPLATE,
    batch_sizes=[1, 16, 24, 32, 48, 64, 512, 1024, 1280])
BERT_LARGE_FP16_PT_384XI32_BATCHES = utils.build_batch_models(
    template=BERT_LARGE_FP16_PT_384XI32_BATCH_TEMPLATE,
    batch_sizes=[1, 16, 24, 32, 48, 64, 512, 1024, 1280])

# ResNet models.
# Model implementation from https://pytorch.org/vision/main/models/resnet.html.
# Batch sizes from MLPerf A100 Configs: https://github.com/mlcommons/inference_results_v2.1/tree/master/closed/NVIDIA/configs/resnet50
RESNET_PT_IMPL = def_types.ModelImplementation(
    id=unique_ids.MODEL_IMPL_RESNET_PT,
    name="RESNET_PT",
    tags=["cnn", "resnet"],
    framework_type=def_types.ModelFrameworkType.PYTORCH,
    module_path=f"{utils.MODELS_MODULE_PATH}.pt.resnet.resnet_model",
    source_info="https://pytorch.org/vision/main/models/resnet.html",
)

RESNET50_FP32_PT_3X224X224XF32_BATCH_TEMPLATE = utils.ModelTemplate(
    id=utils.BATCH_ID(unique_ids.MODEL_RESNET50_FP32_PT_3X224X224XF32),
    name=utils.BATCH_NAME("RESNET50_FP32_PT_3X224X224XF32"),
    tags=[utils.BATCH_TAG],
    model_impl=RESNET_PT_IMPL,
    model_parameters={
        "batch_size": utils.BATCH_SIZE_PARAM,
        "data_type": "fp32",
        "model_name": "torchvision/resnet50",
        "import_on_gpu": False,
        "import_with_fx": True,
    },
    artifacts={
        def_types.ModelArtifactType.LINALG_MLIR:
            utils.ModelArtifactTemplate(
                artifact_type=def_types.ModelArtifactType.STABLEHLO_MLIR,
                source_url=string.Template(
                    PARENT_GCS_DIR +
                    "RESNET50_FP32_PT_3X224X224XF32_BATCH${batch_size}/linalg.mlirbc"
                ),
            ),
    })
RESNET50_FP16_PT_3X224X224XF16_BATCH_TEMPLATE = utils.ModelTemplate(
    id=utils.BATCH_ID(unique_ids.MODEL_RESNET50_FP16_PT_3X224X224XF16),
    name=utils.BATCH_NAME("RESNET50_FP16_PT_3X224X224XF16"),
    tags=[utils.BATCH_TAG],
    model_impl=RESNET_PT_IMPL,
    model_parameters={
        "batch_size": utils.BATCH_SIZE_PARAM,
        "data_type": "fp16",
        "model_name": "torchvision/resnet50",
        "import_on_gpu": True,
        "import_with_fx": False,
    },
    artifacts={
        def_types.ModelArtifactType.LINALG_MLIR:
            utils.ModelArtifactTemplate(
                artifact_type=def_types.ModelArtifactType.STABLEHLO_MLIR,
                source_url=string.Template(
                    PARENT_GCS_DIR +
                    "RESNET50_FP16_PT_3X224X224XF16_BATCH${batch_size}/linalg.mlirbc"
                ),
            ),
    })

RESNET50_FP32_PT_3X224X224XF32_BATCHES = utils.build_batch_models(
    template=RESNET50_FP32_PT_3X224X224XF32_BATCH_TEMPLATE,
    batch_sizes=[1, 8, 64, 128, 256, 2048])
RESNET50_FP16_PT_3X224X224XF16_BATCHES = utils.build_batch_models(
    template=RESNET50_FP16_PT_3X224X224XF16_BATCH_TEMPLATE,
    batch_sizes=[1, 8, 64, 128, 256, 2048])

ALL_MODELS = list(
    itertools.chain(
        BERT_LARGE_FP32_PT_384XI32_BATCHES.values(),
        BERT_LARGE_FP16_PT_384XI32_BATCHES.values(),
        RESNET50_FP32_PT_3X224X224XF32_BATCHES.values(),
        RESNET50_FP16_PT_3X224X224XF16_BATCHES.values(),
    ))
