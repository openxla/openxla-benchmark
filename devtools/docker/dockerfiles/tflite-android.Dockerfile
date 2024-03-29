# Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# An image for cross-compiling towards Android that is compatible with Tensorflow.

FROM gcr.io/iree-oss/openxla-benchmark/android@sha256:cba9827bc47a6afb575efc72ed821ceda32b3132a406235d3edf6d125deef0d7

######## Android SDK ########
ENV ANDROID_SDK "/usr/src/android-sdk"

ENV ANDROID_SDK_API_LEVEL=33
WORKDIR /install-sdk

RUN mkdir "${ANDROID_SDK}"

RUN wget "https://dl.google.com/android/repository/platform-33-ext3_r03.zip" \
    && mkdir -p "${ANDROID_SDK}/platforms/android-${ANDROID_SDK_API_LEVEL}" \
    && unzip "platform-33-ext3_r03.zip" \
    && cp -r android-13/* "${ANDROID_SDK}/platforms/android-${ANDROID_SDK_API_LEVEL}/" \
    && wget "https://dl.google.com/android/repository/sources-33_r01.zip" \
    && mkdir -p "${ANDROID_SDK}/sources/android-${ANDROID_SDK_API_LEVEL}" \
    && unzip "sources-33_r01.zip" \
    && cp -r src/* "${ANDROID_SDK}/sources/android-${ANDROID_SDK_API_LEVEL}/" \
    && rm -rf /install-sdk

WORKDIR /

######## Android SDK Tools ########

ENV ANDROID_BUILD_TOOLS_VERSION "34.0.0"
WORKDIR /install-sdk-tools

RUN wget "https://dl.google.com/android/repository/platform-tools_r34.0.5-linux.zip" \
    && unzip -q "platform-tools_r34.0.5-linux.zip" -d "${ANDROID_SDK}" \
    && wget "https://dl.google.com/android/repository/build-tools_r34-linux.zip" \
    && mkdir -p "${ANDROID_SDK}/build-tools/${ANDROID_BUILD_TOOLS_VERSION}" \
    && unzip -q "build-tools_r34-linux.zip" \
    && cp -r android-14/* "${ANDROID_SDK}/build-tools/${ANDROID_BUILD_TOOLS_VERSION}/" \
    && rm -rf /install-sdk-tools

WORKDIR /
