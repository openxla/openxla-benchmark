#!/usr/bin/env python
## Copyright 2023 The OpenXLA Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import argparse
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

from db_import import config
from db_import import deploy
from db_import import download
from db_import import batch_import
from db_import import process
from db_import import verify

parser = argparse.ArgumentParser(prog="cli",
                                 description="Manages the cloud functions")
parser.add_argument(
    "-F",
    "--config-file",
    help=
    "Read configuration from the given file. The default is <SCRIPT_DIR>/config.yml",
    type=pathlib.Path,
    default=SCRIPT_DIR / "config.yml",
)
subparsers = parser.add_subparsers(required=True)

config_parser = subparsers.add_parser(
    "config", help="Various function for managing config files")
config.configure_parser(config_parser)

deploy_parser = subparsers.add_parser("deploy",
                                      help="Deploy one or more cloud functions")
deploy.configure_parser(deploy_parser)

download_parser = subparsers.add_parser(
    "download", help="Download files from bucket for local usage")
download.configure_parser(download_parser)

batch_import_parser = subparsers.add_parser(
    "batch_import", help="Batch import an entire bucket")
batch_import.configure_parser(batch_import_parser)

process_parser = subparsers.add_parser(
    "process", help="Process a single file from a bucket")
process.configure_parser(process_parser)

verify_parser = subparsers.add_parser(
    "verify", help="Runs integration tests for a given pipeline")
verify.configure_parser(verify_parser)

args = parser.parse_args()

with open(args.config_file) as fd:
  config_file = config.load_config(fd)

args.command_handler(config_file, args)
