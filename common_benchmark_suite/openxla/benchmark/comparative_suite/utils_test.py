# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import string
import unittest

from openxla.benchmark import def_types
from openxla.benchmark.comparative_suite import utils


class UtilsTest(unittest.TestCase):

  def test_build_batch_models(self):
    dummy_impl = def_types.ModelImplementation(
        name="TEST",
        tags=["fp32"],
        framework_type=def_types.ModelFrameworkType.JAX,
        module_path=f"test.model",
        source_info="")
    template = utils.ModelTemplate(
        name=utils.BATCH_NAME("TEST_MODEL"),
        tags=[utils.BATCH_TAG, "test"],
        model_impl=dummy_impl,
        model_parameters={
            "batch_size": utils.BATCH_SIZE_PARAM,
            "data_type": "fp32",
        },
        artifacts={
            def_types.ModelArtifactType.STABLEHLO_MLIR:
                utils.ModelArtifactTemplate(
                    artifact_type=def_types.ModelArtifactType.STABLEHLO_MLIR,
                    source_url=string.Template("batch_${batch_size}/x.mlirbc"))
        },
    )

    models = utils.build_batch_models(template=template, batch_sizes=[1, 2])

    self.assertEqual(
        models, {
            1:
                def_types.Model(
                    name="TEST_MODEL_BATCH1",
                    tags=["batch-1", "test"],
                    model_impl=dummy_impl,
                    model_parameters={
                        "batch_size": 1,
                        "data_type": "fp32",
                    },
                    artifacts={
                        def_types.ModelArtifactType.STABLEHLO_MLIR:
                            def_types.ModelArtifact(
                                artifact_type=def_types.ModelArtifactType.
                                STABLEHLO_MLIR,
                                source_url="batch_1/x.mlirbc")
                    },
                ),
            2:
                def_types.Model(
                    name="TEST_MODEL_BATCH2",
                    tags=["batch-2", "test"],
                    model_impl=dummy_impl,
                    model_parameters={
                        "batch_size": 2,
                        "data_type": "fp32",
                    },
                    artifacts={
                        def_types.ModelArtifactType.STABLEHLO_MLIR:
                            def_types.ModelArtifact(
                                artifact_type=def_types.ModelArtifactType.
                                STABLEHLO_MLIR,
                                source_url="batch_2/x.mlirbc")
                    },
                ),
        })


if __name__ == "__main__":
  unittest.main()
