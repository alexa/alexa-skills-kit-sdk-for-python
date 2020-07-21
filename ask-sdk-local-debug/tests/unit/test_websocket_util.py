# -*- coding: utf-8 -*-
#
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights
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
import os
from mock import patch

from ask_sdk_local_debug.client.autobahn_client import AutobahnClient
from ask_sdk_local_debug.config.skill_invoker_config import \
    SkillInvokerConfiguration
from ask_sdk_local_debug.config.client_config import ClientConfiguration
from ask_sdk_local_debug.config.websocket_config import WebSocketConfiguration
from ask_sdk_local_debug.util import websocket_util
from ask_sdk_local_debug.util.websocket_util import (
    create_client_configuration, create_skill_invoker_config,
    create_web_socket_client, create_web_socket_configuration)


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestWebSocketUtils(unittest.TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_SKILL_FILE_PATH = os.path.join(TEST_DIR, 'data/test_lambda.py')
    TEST_SKILL_HANDLER = "test_lambda_handler"
    TEST_SKILL_ID = "Skill ID 123234"
    TEST_ACCESS_TOKEN = "test Access Token"

    def setUp(self):
        self.test_parsed_args = Namespace(access_token=self.TEST_ACCESS_TOKEN,
                                          skill_id=self.TEST_SKILL_ID,
                                          skill_file_path=self.TEST_SKILL_FILE_PATH,
                                          skill_handler=self.TEST_SKILL_HANDLER)

        self.test_headers = dict(authorization=self.TEST_ACCESS_TOKEN,
                                 upgrade='websocket', connection='upgrade')

    def test_create_web_socket_client(self):
        test_web_socket_client = create_web_socket_client(
            parsed_args=self.test_parsed_args)
        self.assertIsInstance(test_web_socket_client, AutobahnClient,
                              "create_web_socket_client failed to return "
                              "Autobahn client instance.")
        self.assertIsInstance(test_web_socket_client.web_socket_config,
                              WebSocketConfiguration,
                              "create_web_socket_client failed to create "
                              "web_socket_config instance.")
        self.assertIsInstance(
            test_web_socket_client.factory.skill_invoker_config,
            SkillInvokerConfiguration,
            "create_web_socket_client failed to create "
            "skill_invoker_config instance.")

    @patch(
        'ask_sdk_local_debug.util.websocket_util.create_client_configuration')
    def test_create_web_socket_configuration_with_access_token(self,
                                                               mock_client):
        mock_client.return_value.skill_id = self.TEST_SKILL_ID

        test_uri = websocket_util.DEBUG_ENDPOINT_URI.format(self.TEST_SKILL_ID)

        web_socket_config = create_web_socket_configuration(
            parsed_args=self.test_parsed_args)
        self.assertIsInstance(web_socket_config, WebSocketConfiguration,
                              ("create_web_socket_configuration initialized "
                               "invalid WebSocketConfiguration instance."))
        self.assertDictEqual(web_socket_config.headers, self.test_headers)
        self.assertEqual(web_socket_config.web_socket_server_uri, test_uri)

    def test_create_client_configuration(self):
        client_config = create_client_configuration(self.test_parsed_args)

        self.assertIsInstance(client_config, ClientConfiguration,
                              ("create_client_configuration initialized "
                               "invalid ClientConfiguration instance."))
        self.assertEqual(client_config.access_token, self.TEST_ACCESS_TOKEN)
        self.assertEqual(client_config.skill_id, self.TEST_SKILL_ID)
        self.assertEqual(client_config.skill_file_path,
                         self.TEST_SKILL_FILE_PATH)
        self.assertEqual(client_config.skill_handler, self.TEST_SKILL_HANDLER)

    def test_create_skill_invoker_config(self):
        skill_invoker = create_skill_invoker_config(self.test_parsed_args)

        self.assertIsInstance(skill_invoker, SkillInvokerConfiguration,
                              ("create_skill_invoker_config initialized "
                               "invalid SkillInvoker Configuration instance."))
        self.assertEqual(skill_invoker.skill_handler, self.TEST_SKILL_HANDLER)
        self.assertEqual(skill_invoker.skill_file_path,
                         self.TEST_SKILL_FILE_PATH)
