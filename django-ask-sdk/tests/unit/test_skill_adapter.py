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
import os
import sys

from django_ask_sdk.skill_adapter import SkillAdapter
from django.http import JsonResponse, HttpRequest
from ask_sdk_core.skill import CustomSkill
from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_model.response_envelope import ResponseEnvelope
from ask_sdk_webservice_support.webservice_handler import (
    WebserviceSkillHandler)
from ask_sdk_webservice_support.verifier import VerificationException

try:
    import mock
except ImportError:
    from unittest import mock


class TestSkillAdapter(unittest.TestCase):
    def setUp(self):
        sys.path.insert(
            0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unit.test_settings')
        self.mock_skill = mock.MagicMock(spec=CustomSkill)
        self.mock_skill.custom_user_agent = ""

        test_http_request = mock.MagicMock(spec=HttpRequest)
        test_http_request.META = {}
        test_http_request.method = "POST"
        test_http_request.path = "/"
        test_http_request.content_type = "application/json"
        test_http_request.data = {}
        self.mock_http_request = test_http_request

    def test_invalid_skill_instance_throw_exception(self):
        with self.assertRaises(TypeError) as exc:
            SkillAdapter(skill=None)

        self.assertIn(
            "Invalid skill instance provided", str(exc.exception),
            "SkillAdapter constructor didn't throw exception for "
            "invalid skill input")

    def test_add_custom_user_agent_to_valid_skill_initialization(self):
        SkillAdapter(skill=self.mock_skill, verify_signature=False,
                     verify_timestamp=False)

        self.assertIn(
            "django-ask-sdk", self.mock_skill.custom_user_agent,
            "SkillAdapter didn't update custom user agent "
            "for a valid custom skill")
    
    def test_unset_verify_signature_on_init(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, verify_signature=False)
        
        self.assertEqual(
            len(test_skill_adapter._verifiers), 0,
            "SkillAdapter constructor set incorrect verifiers when "
            "request_signature value is provided as False")

    def test_request_dispatch_http_get_throw_method_not_allowed(self):
        self.mock_http_request.method = "GET"

        test_http_response = SkillAdapter.as_view(
            skill=self.mock_skill)(self.mock_http_request)

        self.assertEqual(
            test_http_response.status_code, 405,
            "SkillAdapter view didn't raise method not allowed exception "
            "when a HTTP GET request is passed to it.")

    def test_request_dispatch_verification_failure_throw_exception(self):
        mocked_handler = mock.MagicMock(spec=WebserviceSkillHandler)
        mocked_handler.verify_request_and_dispatch.side_effect = \
            VerificationException("test")
        with mock.patch(
                "django_ask_sdk.skill_adapter.WebserviceSkillHandler",
                return_value=mocked_handler):
            test_http_response = SkillAdapter.as_view(
                skill=self.mock_skill)(self.mock_http_request)

            self.assertEqual(
                test_http_response.status_code, 400,
                "SkillAdapter didn't raise bad request when input "
                "verification failed")

    def test_request_dispatch_failure_throw_exception(self):
        mocked_handler = mock.MagicMock(spec=WebserviceSkillHandler)
        mocked_handler.verify_request_and_dispatch.side_effect = \
            AskSdkException("test")
        with mock.patch(
                "django_ask_sdk.skill_adapter.WebserviceSkillHandler",
                return_value=mocked_handler):
            test_http_response = SkillAdapter.as_view(
                skill=self.mock_skill)(self.mock_http_request)

            self.assertEqual(
                test_http_response.status_code, 500,
                "SkillAdapter didn't raise internal error when "
                "skill invocation failed")

    def test_request_dispatch(self):
        mocked_handler = mock.MagicMock(spec=WebserviceSkillHandler)
        expected_response = ResponseEnvelope().to_dict()
        mocked_handler.verify_request_and_dispatch.return_value = \
            expected_response
        expected_json_response = JsonResponse(data=expected_response)
        with mock.patch(
                "django_ask_sdk.skill_adapter.WebserviceSkillHandler",
                return_value=mocked_handler):
            actual_response = SkillAdapter.as_view(
                skill=self.mock_skill)(self.mock_http_request)

            self.assertEqual(
                actual_response.status_code, 200,
                "SkillAdapter didn't return valid status code "
                "during successful skill dispatch")
            self.assertEqual(
                actual_response.content, expected_json_response.content,
                "SkillAdapter didn't return correct response on "
                "successful skill dispatch")

    def tearDown(self):
        os.environ.pop("DJANGO_SETTINGS_MODULE")
