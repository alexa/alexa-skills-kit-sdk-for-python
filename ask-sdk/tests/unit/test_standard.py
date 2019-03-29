# -*- coding: utf-8 -*-
#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.
#
import unittest

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

try:
    import mock
except ImportError:
    from unittest import mock  # type: ignore


class TestStandardSkillBuilder(unittest.TestCase):
    def test_default_api_client_set(self):
        test_skill_builder = StandardSkillBuilder()

        actual_skill_config = test_skill_builder.skill_configuration

        assert isinstance(actual_skill_config.api_client, DefaultApiClient), (
            "Standard Skill Builder didn't set the api client to the default"
            "implementation")

    def test_persistence_adapter_default_null(self):
        test_skill_builder = StandardSkillBuilder()

        actual_skill_config = test_skill_builder.skill_configuration

        assert actual_skill_config.persistence_adapter is None, (
            "Standard Skill Builder didn't set Persistence Adapter to None "
            "when no table_name is provided")

    def test_persistence_adapter_set(self):
        test_table_name = "TestTable"
        test_dynamodb_resource = mock.Mock()
        test_partition_keygen = mock.Mock()
        test_auto_create_table = False

        test_skill_builder = StandardSkillBuilder(
            table_name=test_table_name,
            auto_create_table=test_auto_create_table,
            partition_keygen=test_partition_keygen,
            dynamodb_client=test_dynamodb_resource)

        actual_skill_config = test_skill_builder.skill_configuration
        actual_adapter = actual_skill_config.persistence_adapter

        assert isinstance(
            actual_adapter, DynamoDbAdapter), (
            "Standard Skill Builder set incorrect persistence adapter in "
            "skill configuration")

        assert actual_adapter.table_name == test_table_name, (
            "Standard Skill Builder set persistence adapter with incorrect "
            "table name in skill configuration")
        assert actual_adapter.partition_keygen == test_partition_keygen, (
            "Standard Skill Builder set persistence adapter with incorrect "
            "partition key generator function in skill configuration")
        assert actual_adapter.create_table == test_auto_create_table, (
            "Standard Skill Builder set persistence adapter with incorrect "
            "auto create table flag in skill configuration")
        assert actual_adapter.dynamodb == test_dynamodb_resource, (
            "Standard Skill Builder set persistence adapter with incorrect "
            "dynamo db resource in skill configuration")
