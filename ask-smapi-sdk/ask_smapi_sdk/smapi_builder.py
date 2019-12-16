# -*- coding: utf-8 -*-
#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights
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
from abc import ABCMeta, abstractmethod

from ask_sdk_model_runtime import (DefaultApiClient, DefaultSerializer,
                                   ApiConfiguration,
                                   AuthenticationConfiguration)
from ask_smapi_model.services.skill_management import (
    SkillManagementServiceClient)

if typing.TYPE_CHECKING:
    from ask_sdk_model_runtime import ApiClient, Serializer

DEFAULT_API_ENDPOINT = "https://api.amazonalexa.com"


class SmapiClientBuilder(object):
    """Abstract SmapiClient Builder for building
    :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
    object.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        # type: () -> None
        """Abstract SmapiClient Builder for building
        :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        object.
        """
        self._api_endpoint = None  # type: str

    @property
    def api_endpoint(self):
        # type: () -> str
        """Returns the Endpoint to hit by the SMAPI Service.

        :return: Endpoint to hit by the SMAPI service client.
        :rtype: str
        """
        return self._api_endpoint

    @api_endpoint.setter
    def api_endpoint(self, value):
        # type: (str) -> None
        """Sets the Endpoint value to hit by the SMAPI Service.

        :param value: Endpoint to hit by the SMAPI service client.
        :type value: str
        """
        self._api_endpoint = value

    @abstractmethod
    def client(self):
        # type: () -> SkillManagementServiceClient
        raise NotImplementedError





