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


class StandardSmapiClientBuilder(SmapiClientBuilder):
    """Standard SmapiClient Builder class used to generate
    :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
    object with default Serializer and ApiClient implementations.

    :param client_id: The ClientId value from LWA profiles.
    :type client_id: str
    :param client_secret: The ClientSecret value from LWA profiles.
    :type client_secret: str
    :param refresh_token: Client refresh_token required to get access token
        for API calls.
    :type refresh_token: str
    """

    def __init__(self, client_id, client_secret, refresh_token):
        # type: (str, str, str) -> None
        """Smapi Builder class used to generate
        :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        object with default Serializer and ApiClient implementations.

        :param client_id: The ClientId value from LWA profiles.
        :type client_id: str
        :param client_secret: The ClientSecret value from LWA profiles.
        :type client_secret: str
        :param refresh_token: Client refresh_token required to get access token
        for API calls.
        """
        super(StandardSmapiClientBuilder, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def client(self):
        # type: () -> SkillManagementServiceClient
        """Creates the smapi client object using AuthenticationConfiguration
        and ApiConfiguration registered values.

        :return: A smapi object that can be used for making SMAPI method
            invocations.
        :rtype: :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        """
        if self.api_endpoint is None:
            self.api_endpoint = DEFAULT_API_ENDPOINT

        api_configuration = ApiConfiguration(serializer=DefaultSerializer(),
                                             api_client=DefaultApiClient(),
                                             api_endpoint=self.api_endpoint)

        authentication_configuration = AuthenticationConfiguration(
            client_id=self.client_id, client_secret=self.client_secret,
            refresh_token=self.refresh_token)

        return SkillManagementServiceClient(
            api_configuration=api_configuration,
            authentication_configuration=authentication_configuration)


class CustomSmapiClientBuilder(SmapiClientBuilder):
    """Smapi Custom Builder with serializer, api_client and api_endpoint setter
    functions.

    This builder is used to create an instance of
    :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
    with default Serializers and ApiClient implementations.
    """

    def __init__(self, client_id, client_secret, refresh_token,
                 serializer=None, api_client=None):
        # type: (str, str, str, Serializer, ApiClient) -> None
        """Smapi Custom Builder with serializer, api_client and api_endpoint
        setter functions.

        This builder is used to create an instance of
        :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        with default Serializers and ApiClient implementations.

        :param client_id: The ClientId value from LWA profiles.
        :type client_id: str
        :param client_secret: The ClientSecret value from LWA profiles.
        :type client_secret: str
        :param refresh_token: Client refresh_token required to get access token
        for API calls.
        :param serializer: serializer implementation for encoding/decoding JSON
            from/to Object models.
        :type serializer: (optional) ask_sdk_model_runtime.serializer.Serializer
        :param api_client: API Client implementation
        :type api_client: (optional) ask_sdk_model_runtime.api_client.ApiClient
        """
        super(CustomSmapiClientBuilder, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.serializer = serializer
        self.api_client = api_client

    def client(self):
        # type: () -> SkillManagementServiceClient
        """Creates the smapi client object using AuthenticationConfiguration
        and ApiConfiguration registered values.

        :return: A smapi object that can be used for making SMAPI method
            invocations.
        :rtype: :py:class:`ask_smapi_model.services.skill_management.SkillManagementServiceClient`
        """
        if self.serializer is None:
            self.serializer = DefaultSerializer()
        if self.api_client is None:
            self.api_client = DefaultApiClient()
        if self.api_endpoint is None:
            self.api_endpoint = DEFAULT_API_ENDPOINT

        api_configuration = ApiConfiguration(serializer=self.serializer,
                                             api_client=self.api_client,
                                             api_endpoint=self.api_endpoint)

        authentication_configuration = AuthenticationConfiguration(
            client_id=self.client_id, client_secret=self.client_secret,
            refresh_token=self.refresh_token)

        return SkillManagementServiceClient(
            api_configuration=api_configuration,
            authentication_configuration=authentication_configuration)
