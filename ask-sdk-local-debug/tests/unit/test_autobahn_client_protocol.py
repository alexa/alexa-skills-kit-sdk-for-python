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
import json
from mock import patch, Mock

from ask_sdk_local_debug.client.autobahn_client_protocol import AutobahnClientProtocol

TEST_REQUEST_DATA = ("{\n    \"version\": \"fooversion\",\n"
                     "    \"type\": \"SkillRequestMessage\",\n"
                     "    \"requestId\": \"foorequestid\",\n"
                     "    \"requestPayload\": \"foorequestpayload\"\n}")

TEST_SUCCESS_RESPONSE = ("{\n    \"version\": \"fooversion\",\n"
                         "    \"type\": \"SkillResponseSuccessMessage\",\n"
                         "    \"originalRequestId\": \"foorequestid\",\n"
                         "    \"responsePayload\": \"TestPayload\"\n}")

TEST_FAILURE_RESPONSE = ("{\n   \"version\": \"fooversion\",\n"
                         "    \"type\": \"SkillResponseFailureMessage\",\n"
                         "    \"originalRequestId\": \"foorequestid\",\n"
                         "   \"errorCode\": \"500\",\n"
                         "    \"errorMessage\": \"mock error\"\n}")

TEST_DESERIALIZE_DATA = ("{\"version\": \"fooversion\", "
                         "\"object_type\": \"SkillRequestMessage\", "
                         "\"request_id\": \"foorequestid\", "
                         "\"request_payload\": \"foorequestpayload\"}")


def mock_skill_response(local_debug_request, skill_invoker):
    test_request = json.dumps(local_debug_request.to_dict())
    if test_request == TEST_DESERIALIZE_DATA:
        return TEST_SUCCESS_RESPONSE
    return TEST_FAILURE_RESPONSE


TEST_REQUEST_DATA = ("{\n    \"version\": \"fooversion\",\n"
                     "    \"type\": \"SkillRequestMessage\",\n"
                     "    \"requestId\": \"foorequestid\",\n"
                     "    \"requestPayload\": \"foorequestpayload\"\n}")

TEST_SUCCESS_RESPONSE = ("{\n    \"version\": \"fooversion\",\n"
                         "    \"type\": \"SkillResponseSuccessMessage\",\n"
                         "    \"originalRequestId\": \"foorequestid\",\n"
                         "    \"responsePayload\": \"TestPayload\"\n}")

TEST_FAILURE_RESPONSE = ("{\n   \"version\": \"fooversion\",\n"
                         "    \"type\": \"SkillResponseFailureMessage\",\n"
                         "    \"originalRequestId\": \"foorequestid\",\n"
                         "   \"errorCode\": \"500\",\n"
                         "    \"errorMessage\": \"mock error\"\n}")

TEST_DESERIALIZE_DATA = ("{\"version\": \"fooversion\", "
                         "\"object_type\": \"SkillRequestMessage\", "
                         "\"request_id\": \"foorequestid\", "
                         "\"request_payload\": \"foorequestpayload\"}")


def mock_skill_response(local_debug_request, skill_invoker_config):
    test_request = json.dumps(local_debug_request.to_dict())
    if test_request == TEST_DESERIALIZE_DATA:
        return TEST_SUCCESS_RESPONSE
    return TEST_FAILURE_RESPONSE


class TestAutobahnClientProtocol(unittest.TestCase):

    def setUp(self):
        self.test_client_protocol = AutobahnClientProtocol()
        self.test_client_protocol.factory = Mock()

    @patch(
        'ask_sdk_local_debug.client.autobahn_client_protocol.get_skill_response',
        side_effect=mock_skill_response)
    @patch.object(AutobahnClientProtocol, 'send_skill_response')
    def test_on_message_successful_skill_response(self,
                                                  mock_send_skill_response,
                                                  _skill_response):
        self.test_client_protocol.onMessage(
            skill_request_payload=TEST_REQUEST_DATA.encode('utf-8'),
            is_binary=False)

        mock_send_skill_response.assert_called_once_with(
            local_debug_ask_response=TEST_SUCCESS_RESPONSE)

    @patch(
        'ask_sdk_local_debug.client.autobahn_client_protocol.get_skill_response',
        side_effect=mock_skill_response)
    @patch.object(AutobahnClientProtocol, 'send_skill_response')
    def test_on_message_failure_skill_response(self, mock_send_skill_response,
                                               _skill_response):
        test_data = "{\"version\": \"fooversion\",\"request\":\"test\"}"

        self.test_client_protocol.onMessage(
            skill_request_payload=test_data.encode('utf-8'), is_binary=True)

        mock_send_skill_response.assert_called_once_with(
            local_debug_ask_response=TEST_FAILURE_RESPONSE)

    @patch.object(AutobahnClientProtocol, 'sendMessage')
    def test_send_skill_response(self, mock_send_message):
        test_encoded_message = TEST_SUCCESS_RESPONSE.encode('utf8')

        self.test_client_protocol.send_skill_response(
            local_debug_ask_response=TEST_SUCCESS_RESPONSE)

        mock_send_message.assert_called_once_with(test_encoded_message)
