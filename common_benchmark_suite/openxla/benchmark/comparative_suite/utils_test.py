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
        artifacts_dir_url=string.Template("test/${name}/batch_${batch_size}"),
        exported_model_types=[def_types.ModelArtifactType.STABLEHLO_MLIR],
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
                    artifacts_dir_url="test/TEST_MODEL_BATCH1/batch_1",
                    exported_model_types=[
                        def_types.ModelArtifactType.STABLEHLO_MLIR
                    ],
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
                    artifacts_dir_url="test/TEST_MODEL_BATCH2/batch_2",
                    exported_model_types=[
                        def_types.ModelArtifactType.STABLEHLO_MLIR
                    ],
                ),
        })

  def test_build_batch_models_with_defaults(self):
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
                    artifacts_dir_url=None,
                    exported_model_types=[],
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
                    artifacts_dir_url=None,
                    exported_model_types=[],
                ),
        })

  def test_build_batch_benchmark_cases(self):
    dummy_impl = def_types.ModelImplementation(
        name="TEST",
        tags=["fp32"],
        framework_type=def_types.ModelFrameworkType.JAX,
        module_path=f"test.model",
        source_info="")
    batch_models = {
        1:
            def_types.Model(
                name="TEST_MODEL_BATCH1",
                tags=["batch-1", "test"],
                model_impl=dummy_impl,
                model_parameters={
                    "batch_size": 1,
                    "data_type": "fp32",
                },
                artifacts_dir_url=None,
                exported_model_types=[],
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
                artifacts_dir_url=None,
                exported_model_types=[],
            ),
    }
    input_data = def_types.ModelTestData(
        name="test_image",
        source_url="https://example.com/test.image",
    )
    verify_parameters = {"tolerance": 0.1}

    cases = utils.build_batch_benchmark_cases(
        batch_models=batch_models,
        input_data=input_data,
        verify_parameters=verify_parameters,
        batch_sizes=[1, 2])

    self.assertEqual(
        cases, {
            1:
                def_types.BenchmarkCase.build(
                    model=batch_models[1],
                    input_data=input_data,
                    verify_parameters=verify_parameters),
            2:
                def_types.BenchmarkCase.build(
                    model=batch_models[2],
                    input_data=input_data,
                    verify_parameters=verify_parameters),
        })


if __name__ == "__main__":
  unittest.main()
