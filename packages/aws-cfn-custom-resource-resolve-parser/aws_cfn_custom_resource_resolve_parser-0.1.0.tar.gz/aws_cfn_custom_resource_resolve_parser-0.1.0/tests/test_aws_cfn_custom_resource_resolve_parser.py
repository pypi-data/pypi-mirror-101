#!/usr/bin/env python

"""Tests for `aws_cfn_custom_resource_resolve_parser` package."""

import pytest
import boto3
from os import path


from aws_cfn_custom_resource_resolve_parser import parse_secret_resolve_string


def test_parsing_arn():
    secret = r"{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:/kafka/eu-west-1/lkc-y6xwp/cc.johnmille-uxPVuS:SecretString:BOOTSTRAP_SERVERS}}"
    secret_value = parse_secret_resolve_string(secret)
    assert (
        secret_value[0]
        == "arn:aws:secretsmanager:eu-west-1:012345678912:secret:/kafka/eu-west-1/lkc-y6xwp/cc.johnmille-uxPVuS"
    )
    assert secret_value[1] == "BOOTSTRAP_SERVERS"


def test_parsing_name():
    secret = r"{{resolve:secretsmanager:/kafka/eu-west-1/lkc-y6xwp/cc.johnmille-uxPVuS:SecretString:BOOTSTRAP_SERVERS:AWSPENDING}}"
    secret_value = parse_secret_resolve_string(secret)
    assert secret_value[0] == "/kafka/eu-west-1/lkc-y6xwp/cc.johnmille-uxPVuS"
    assert secret_value[1] == "BOOTSTRAP_SERVERS"
    assert secret_value[2] == "AWSPENDING"
