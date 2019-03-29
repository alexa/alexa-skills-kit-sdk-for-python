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
import json
import typing

from ask_sdk_model import RequestEnvelope

from ask_sdk_runtime.skill_builder import AbstractSkillBuilder

from .skill import CustomSkill, SkillConfiguration

if typing.TYPE_CHECKING:
    from typing import Callable, TypeVar, Dict
    from ask_sdk_model.services import ApiClient
    from .attributes_manager import AbstractPersistenceAdapter
    T = TypeVar('T')


class SkillBuilder(AbstractSkillBuilder):
    """Skill Builder with helper functions for building
    :py:class:`ask_sdk_core.skill.Skill` object.
    """

    def __init__(self):
        # type: () -> None
        super(SkillBuilder, self).__init__()
        self.custom_user_agent = None
        self.skill_id = None

    @property
    def skill_configuration(self):
        # type: () -> SkillConfiguration
        """Create the skill configuration object using the
        registered components.
        """
        self.runtime_configuration = self.runtime_configuration_builder.get_runtime_configuration()
        self.runtime_configuration.custom_user_agent = self.custom_user_agent
        self.runtime_configuration.skill_id = self.skill_id
        self.runtime_configuration = self.__populate_missing_attributes(
            self.runtime_configuration)

        return self.runtime_configuration

    def __populate_missing_attributes(self, config):
        # type: (SkillConfiguration) -> SkillConfiguration
        if not hasattr(config, 'persistence_adapter'):
            config.persistence_adapter = None

        if not hasattr(config, 'api_client'):
            config.api_client = None

        return config

    def create(self):
        # type: () -> CustomSkill
        """Create a skill object using the registered components.

        :return: a skill object that can be used for invocation.
        :rtype: Skill
        """
        skill_configuration = self.skill_configuration

        return CustomSkill(skill_configuration=skill_configuration)

    def lambda_handler(self):
        # type: () -> Callable[[RequestEnvelope, T], Dict[str, T]]
        """Create a handler function that can be used as handler in
        AWS Lambda console.

        The lambda handler provides a handler function, that acts as
        an entry point to the AWS Lambda console. Users can set the
        lambda_handler output to a variable and set the variable as
        AWS Lambda Handler on the console.

        :return: Handler function to tag on AWS Lambda console.
        """
        def wrapper(event, context):
            # type: (RequestEnvelope, T) -> Dict[str, T]
            skill = CustomSkill(skill_configuration=self.skill_configuration)
            request_envelope = skill.serializer.deserialize(
                payload=json.dumps(event), obj_type=RequestEnvelope)
            response_envelope = skill.invoke(
                request_envelope=request_envelope, context=context)
            return skill.serializer.serialize(response_envelope)
        return wrapper


class CustomSkillBuilder(SkillBuilder):
    """Skill Builder with api client and persistence adapter setter
    functions.
    """

    def __init__(self, persistence_adapter=None, api_client=None):
        # type: (AbstractPersistenceAdapter, ApiClient) -> None
        """Skill Builder with api client and persistence adapter
        setter functions.
        """
        super(CustomSkillBuilder, self).__init__()
        self.persistence_adapter = persistence_adapter
        self.api_client = api_client

    @property
    def skill_configuration(self):
        # type: () -> SkillConfiguration
        """Create the skill configuration object using the
        registered components.
        """
        skill_config = super(CustomSkillBuilder, self).skill_configuration
        skill_config.persistence_adapter = self.persistence_adapter
        skill_config.api_client = self.api_client
        return skill_config
