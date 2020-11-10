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
import json
import unittest
from unittest import mock
from mock import patch

from ask_sdk_model.dynamic_endpoints import (FailureResponse, Request,
                                             SuccessResponse)

from ask_sdk_local_debug.exception import LocalDebugSdkException
from ask_sdk_local_debug.util.response_util import (
    get_local_debug_success_response, get_local_debug_failure_response,
    get_skill_response, get_deserialized_request)
from ask_sdk_local_debug.util.serializer import Serializer

TEST_RESPONSE_PAYLOAD = {"response_payload": "response msg"}


def mock_success_skill_builder(*args):
    return TEST_RESPONSE_PAYLOAD


def mock_failure_skill_builder(*args):
    def wrapper(*arg):
        raise Exception("Exception msg")

    return wrapper


class TestRequestResponseUtils(unittest.TestCase):
    TEST_VERSION = "testVersion"
    TEST_REQUEST_ID = "testRequestId"
    TEST_PAYLOAD = "Test Payload"
    TEST_EXCEPTION = "Test Exception"
    TEST_REQUEST_PAYLOAD = "{\"request payload\": \"request payload\"}"

    def setUp(self):
        self.test_local_debug_request = Request(
            request_id=self.TEST_REQUEST_ID, version=self.TEST_VERSION,
            request_payload=self.TEST_REQUEST_PAYLOAD)
        self.default_serializer = Serializer.get_instance()

    def test_local_debug_success_response_builder(self):
        success_response = get_local_debug_success_response(
            local_debug_request=self.test_local_debug_request,
            skill_success_response=self.TEST_PAYLOAD)

        self.assertIsInstance(success_response, SuccessResponse)
        self.assertEqual(success_response.version, self.TEST_VERSION)
        self.assertEqual(success_response.response_payload, self.TEST_PAYLOAD)
        self.assertEqual(success_response.original_request_id,
                         self.TEST_REQUEST_ID)
        self.assertEqual(success_response.object_type,
                         "SkillResponseSuccessMessage")

    @patch('ask_sdk_local_debug.util.response_util.SuccessResponse',
           side_effect=Exception('Exception msg'))
    def test_local_debug_success_response_builder_exception(self, _mock_resp):
        with self.assertRaises(LocalDebugSdkException) as exc:
            _success_response = get_local_debug_success_response(
                local_debug_request=self.test_local_debug_request,
                skill_success_response=self.TEST_PAYLOAD)

        self.assertIn(
            "Failed to create SuccessResponse instance : Exception msg",
            str(exc.exception),
            "get_local_debug_success_response didn't raise "
            "LocalDebugSdkException for invalid arguments")

    def test_local_debug_failure_response_builder(self):
        failure_response = get_local_debug_failure_response(
            local_debug_request=self.test_local_debug_request,
            exception=Exception(self.TEST_EXCEPTION))

        self.assertIsInstance(failure_response, FailureResponse)
        self.assertEqual(failure_response.version, self.TEST_VERSION)
        self.assertEqual(failure_response.error_message, self.TEST_EXCEPTION)
        self.assertEqual(failure_response.original_request_id,
                         self.TEST_REQUEST_ID)
        self.assertEqual(failure_response.object_type,
                         "SkillResponseFailureMessage")

    @patch('ask_sdk_local_debug.util.response_util.FailureResponse',
           side_effect=Exception('Exception msg'))
    def test_local_debug_failure_response_builder_exception(self, _mock_resp):
        with self.assertRaises(LocalDebugSdkException) as exc:
            _failure_response = get_local_debug_failure_response(
                local_debug_request=self.test_local_debug_request,
                exception=Exception(self.TEST_EXCEPTION))

        self.assertIn(
            "Failed to create FailureResponse instance : Exception msg",
            str(exc.exception),
            "get_local_debug_failure_response didn't raise "
            "LocalDebugSdkException for invalid arguments")

    def test_failure_get_skill_response(self):
        failure_response = FailureResponse(version=self.TEST_VERSION,
                                           original_request_id=self.TEST_REQUEST_ID,
                                           error_code='500',
                                           error_message='Exception msg')
        test_response = json.dumps(
            self.default_serializer.serialize(failure_response))

        mock_skill_invoker_config = mock.MagicMock()
        mock_skill_invoker_config.skill_builder_func.side_effect = Exception("Exception msg")
        response = get_skill_response(
            local_debug_request=self.test_local_debug_request,
            skill_invoker_config=mock_skill_invoker_config)

        self.assertEqual(response, test_response,
                         "Not a valid Failure Response")

    def test_success_get_skill_response(self):
        success_response = SuccessResponse(version=self.TEST_VERSION,
                                           original_request_id=self.TEST_REQUEST_ID,
                                           response_payload=json.dumps(
                                               TEST_RESPONSE_PAYLOAD))
        test_response = json.dumps(
            self.default_serializer.serialize(success_response))

        mock_skill_invoker_config = mock.MagicMock()
        mock_skill_invoker_config.skill_builder_func.return_value = TEST_RESPONSE_PAYLOAD
        response = get_skill_response(
            local_debug_request=self.test_local_debug_request,
            skill_invoker_config=mock_skill_invoker_config)

        self.assertEqual(response, test_response,
                         "Not a valid Success Response")

    def test_get_skill_response_exception_raised(self):
        with patch('ask_sdk_local_debug.util.response_util.Serializer') as mock_serializer:
            mock_serializer.get_instance.return_value = mock_serializer
            mock_serializer.serialize.side_effect = Exception('Test Exception')
            with self.assertRaises(LocalDebugSdkException) as exc:
                mock_skill_invoker_config = mock.MagicMock()
                mock_skill_invoker_config.skill_builder_func.return_value = TEST_RESPONSE_PAYLOAD
                response = get_skill_response(
                    local_debug_request=self.test_local_debug_request,
                    skill_invoker_config=mock_skill_invoker_config)

            self.assertIn(
                "Error in get_skill_response : {}".format(self.TEST_EXCEPTION),
                str(exc.exception),
                "get_skill_response didn't raise LocalDebugSdkException for "
                "invalid skill invoker config.")

    def test_deserialize_request(self):
        valid_sample_data = ("{\n    \"version\": \"fooversion\",\n"
                             "    \"type\": \"SkillRequestMessage\",\n"
                             "    \"requestId\": \"foorequestid\",\n"
                             "    \"requestPayload\": \"foorequestpayload\"\n}")

        sample_request = get_deserialized_request(
            skill_request_payload=valid_sample_data)

        self.assertEqual(sample_request.version, "fooversion")
        self.assertEqual(sample_request.object_type, "SkillRequestMessage")
        self.assertEqual(sample_request.request_id, "foorequestid")
        self.assertEqual(sample_request.request_payload, "foorequestpayload")

    def test_invalid_deserialize_request(self):
        invalid_sample_data = "{\n    \"version\": \"fooversion\",\n"

        with self.assertRaises(LocalDebugSdkException) as exc:
            sample_request = get_deserialized_request(
                skill_request_payload=invalid_sample_data)
            print(sample_request)
        self.assertIn("Failed to deserialize skill_request : Couldn\'t "
                      "parse response body: {}".format(invalid_sample_data),
                      str(exc.exception), "get_deserialized_request didn't "
                                          "raise LocalDebugSdkException for "
                                          "invalid skill request")
