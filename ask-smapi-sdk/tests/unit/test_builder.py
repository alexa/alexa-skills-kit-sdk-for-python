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
import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from ask_smapi_sdk import (
    SmapiClientBuilder, StandardSmapiClientBuilder, CustomSmapiClientBuilder)
from ask_smapi_model.services.skill_management import (
    SkillManagementServiceClient)
from ask_sdk_model_runtime import (DefaultApiClient, DefaultSerializer,
                                   ApiConfiguration,
                                   AuthenticationConfiguration)

DEFAULT_API_ENDPOINT = "https://api.amazonalexa.com"

class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.test_client_id = 'client_id'
        self.test_client_secret = 'client_secret'
        self.test_refresh_token = 'refresh_token'

    def test_standard_smapi_client_create(self):
        test_standard_builder = StandardSmapiClientBuilder(
            client_id=self.test_client_id,
            client_secret=self.test_client_secret,
            refresh_token=self.test_refresh_token)
        test_client = test_standard_builder.client()
        self.assertIsInstance(test_client, SkillManagementServiceClient,
                              "StandardSmapiClientBuilder client method did "
                              "not create a SkillManagementServiceClient "
                              "instance")

        self.assertEqual(test_standard_builder.api_endpoint, DEFAULT_API_ENDPOINT,
                    "StandardSmapiClientBuilder failed to set default "
                    "Api Endpoint")

    def test_custom_smapi_client_create(self):
        mock_serializer = mock.Mock(spec=DefaultSerializer)
        mock_api_client = mock.Mock(spec=DefaultApiClient)
        test_api_end_point = 'https://amazon.com'
        test_custom_builder = CustomSmapiClientBuilder(
            client_id=self.test_client_id,
            client_secret=self.test_client_secret,
            refresh_token=self.test_refresh_token,
            serializer=mock_serializer,
            api_client=mock_api_client)
        test_custom_builder.api_endpoint = test_api_end_point
        
        test_client = test_custom_builder.client()
        
        self.assertIsInstance(test_client, SkillManagementServiceClient,
                              "CustomSmapiClientBuilder client method did "
                              "not create a SkillManagementServiceClient "
                              "instance")
        self.assertEqual(test_client._serializer,
                         mock_serializer, ("CustomSmapiClientBuilder "
                                           "failed to set custom Serializer"))
        self.assertEqual(test_client._api_client,
                         mock_api_client, ("CustomSmapiClientBuilder "
                                           "failed to set custom ApiClient"))
        self.assertEqual(test_client._api_endpoint,
                    test_api_end_point, ("CustomSmapiClientBuilder "
                                    "failed to set custom Api EndPoint"))