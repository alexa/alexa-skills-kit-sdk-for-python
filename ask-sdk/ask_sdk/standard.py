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
import typing

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

if typing.TYPE_CHECKING:
    from typing import Callable
    from ask_sdk_model import RequestEnvelope
    from ask_sdk_core.skill_builder import SkillConfiguration
    from boto3.resources.base import ServiceResource


class StandardSkillBuilder(SkillBuilder):
    """Skill Builder with api client and db adapter coupling to Skill.

    Standard Skill Builder is an implementation of
    :py:class:`ask_sdk_core.skill_builder.SkillBuilder`
    with coupling of DynamoDb Persistence Adapter settings and a Default
    Api Client added to the :py:class:`ask_sdk_core.skill.Skill`.

    :param table_name: Name of the table to be created or used
    :type table_name: str
    :param auto_create_table: Should the adapter try to create the table if
        it doesn't exist.
    :type auto_create_table: bool
    :param partition_keygen: Callable function that takes a request
        envelope and provides a unique partition key value.
    :type partition_keygen: Callable[[RequestEnvelope], str]
    :param dynamodb_client: Resource to be used, to perform dynamo
        operations.
    :type dynamodb_client: boto3.resources.base.ServiceResource
    """

    def __init__(
            self, table_name=None, auto_create_table=None,
            partition_keygen=None, dynamodb_client=None):
        # type: (str, bool, Callable[[RequestEnvelope], str], ServiceResource) -> None
        """Skill Builder with api client and db adapter coupling to Skill.

        Standard Skill Builder is an implementation of
        :py:class:`ask_sdk_core.skill_builder.SkillBuilder`
        with coupling of DynamoDb Persistence Adapter settings and a Default
        Api Client added to the :py:class:`ask_sdk_core.skill.Skill`.

        :param table_name: Name of the table to be created or used
        :type table_name: str
        :param auto_create_table: Should the adapter try to create the table if
            it doesn't exist.
        :type auto_create_table: bool
        :param partition_keygen: Callable function that takes a request
            envelope and provides a unique partition key value.
        :type partition_keygen: Callable[[ask_sdk_model.RequestEnvelope], str]
        :param dynamodb_client: Resource to be used, to perform dynamo
            operations.
        :type dynamodb_client: boto3.resources.base.ServiceResource
        """
        super(StandardSkillBuilder, self).__init__()
        self.table_name = table_name
        self.auto_create_table = auto_create_table
        self.partition_keygen = partition_keygen
        self.dynamodb_client = dynamodb_client

    @property
    def skill_configuration(self):
        # type: () -> SkillConfiguration
        """Create the skill configuration object using the registered
        components.
        """
        skill_config = super(StandardSkillBuilder, self).skill_configuration
        skill_config.api_client = DefaultApiClient()

        if self.table_name is not None:
            kwargs = {"table_name": self.table_name}
            if self.auto_create_table:
                kwargs["create_table"] = self.auto_create_table

            if self.partition_keygen:
                kwargs["partition_keygen"] = self.partition_keygen

            if self.dynamodb_client:
                kwargs["dynamodb_resource"] = self.dynamodb_client

            skill_config.persistence_adapter = DynamoDbAdapter(**kwargs)
        return skill_config
