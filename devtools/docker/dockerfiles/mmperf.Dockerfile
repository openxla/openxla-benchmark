# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# An image for running mmperf: https://github.com/mmperf/mmperf.
#
# mmperf benchmarks matrix-multiplication workloads on IREE and various backends
# such as OpenBLAS, MKL, TVM, Halide, CuBLAS, etc.
#
# These backends are included either in this image or as a submodule in the
# mmperf repo. Later versions of Clang, LLVM, Python and Ubuntu are needed
# to satisfy the dependency requirements of the backends.

FROM gcr.io/iree-oss/openxla-benchmark/base-python3.10@sha256:e19b4743fe06d0d779fb8a47e5d37112e1a25319dce8e1f381d73a99ed29dac2

######## CUDA ########
RUN apt-get update \
  && apt-get install -y \
    nvidia-cuda-toolkit \
  && mkdir -p "/usr/nvvm/libdevice" \
  && ln -s "/usr/lib/nvidia-cuda-toolkit/libdevice/libdevice.10.bc" "/usr/nvvm/libdevice/libdevice.10.bc"
##############

######## MKL ########
WORKDIR /install-mkl

RUN wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    && apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    && sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list' \
    && apt-get update \
    && apt-get install -y intel-mkl-64bit-2018.2-046 \
    && rm -rf /install-mkl

WORKDIR /

ENV MKL_DIR="/opt/intel/mkl"
##############

######## OPENBLAS ########
RUN apt-get update \
  && apt-get install -y libopenblas-dev
##############

######## BLIS ########
WORKDIR /install-blis

RUN git clone --recurse-submodules https://github.com/flame/blis \
  && cd blis \
  && ./configure --prefix=/opt/blis --enable-cblas -c amd64 \
  && make -j 32 \
  && make install \
  && rm -rf /install-blis

WORKDIR /

ENV BLIS_DIR="/opt/blis"
##############
