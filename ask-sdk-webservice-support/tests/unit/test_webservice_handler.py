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

from ask_sdk_core.skill import CustomSkill
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_webservice_support.webservice_handler import (
    WebserviceSkillHandler)
from ask_sdk_webservice_support.verifier import (
    RequestVerifier, TimestampVerifier, AbstractVerifier,
    VerificationException)

try:
    import mock
except ImportError:
    from unittest import mock


class TestWebserviceSkillHandler(unittest.TestCase):
    def setUp(self):
        self.mock_skill = mock.MagicMock(spec=CustomSkill)
        self.mock_serializer = mock.MagicMock(spec=DefaultSerializer)
        self.mock_skill.serializer = self.mock_serializer
        self.mock_skill.custom_user_agent = ""
        self.mock_verifier = mock.MagicMock(spec=AbstractVerifier)

    def test_webservice_skill_handler_init_invalid_skill_raise_exception(self):
        with self.assertRaises(TypeError) as exc:
            WebserviceSkillHandler(skill=None)

        self.assertIn(
            "Expected a custom skill instance", str(exc.exception),
            "Webservice skill handler didn't raise TypError on "
            "initialization when an invalid skill instance is provided")

    def test_webservice_skill_handler_init_add_custom_user_agent(self):
        WebserviceSkillHandler(skill=self.mock_skill, verify_signature=False,
                               verify_timestamp=False)

        self.assertEqual(
            self.mock_skill.custom_user_agent, " ask-webservice",
            "Webservice skill handler didn't update custom user agent "
            "for a valid custom skill")

    def test_webservice_skill_handler_init_with_no_verifiers(self):
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_signature=False,
            verify_timestamp=False)

        default_verifiers = test_webservice_skill_handler._verifiers

        self.assertEqual(
            len(default_verifiers), 0,
            "Webservice skill handler initialized invalid number of "
            "default verifiers")

    def test_webservice_skill_handler_init_with_default_verifiers(self):
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill)

        default_verifiers = test_webservice_skill_handler._verifiers

        self.assertEqual(
            len(default_verifiers), 2,
            "Webservice skill handler initialized invalid number of "
            "default verifiers")

        for verifier in default_verifiers:
            if not (isinstance(verifier, RequestVerifier) or
                    isinstance(verifier, TimestampVerifier)):
                self.fail(
                    "Webservice skill handler initialized invalid verifier "
                    "when left as default")

    def test_webservice_skill_handler_init_with_verifiers_set_correctly(
            self):
        test_verifier = mock.MagicMock(spec=AbstractVerifier)
        test_verifier.return_value = "Test"
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_signature=None,
            verify_timestamp=None, verifiers=[test_verifier()])

        default_verifiers = test_webservice_skill_handler._verifiers

        self.assertEqual(
            len(default_verifiers), 1,
            "Webservice skill handler initialized invalid number of "
            "verifiers, when an input list is passed")

        for verifier in default_verifiers:
            self.assertEqual(
                verifier, "Test",
                "Webservice skill handler initialized invalid verifier "
                "when an input list is passed")

    def test_webservice_skill_handler_init_default_with_verifiers_set_correctly(
            self):
        test_verifier = mock.MagicMock(spec=AbstractVerifier)
        test_verifier.return_value = "Test"
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verifiers=[test_verifier()])

        default_verifiers = test_webservice_skill_handler._verifiers

        self.assertEqual(
            len(default_verifiers), 3,
            "Webservice skill handler initialized invalid number of "
            "verifiers, when an input list is passed")

    def test_webservice_skill_handler_init_timestamp_check_disabled(self):
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_timestamp=False)

        default_verifiers = test_webservice_skill_handler._verifiers

        self.assertEqual(
            len(default_verifiers), 1,
            "Webservice skill handler initialized invalid number of "
            "default verifiers, when timestamp verification env property is "
            "disabled")

        verifier = default_verifiers[0]
        self.assertIsInstance(
            verifier, RequestVerifier,
            "Webservice skill handler initialized invalid default verifier, "
            "when request timestamp verification env property is set to false")

    def test_webservice_skill_handler_init_signature_check_disabled(self):
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_signature=False)

        default_verifiers = test_webservice_skill_handler._verifiers

        self.assertEqual(
            len(default_verifiers), 1,
            "Webservice skill handler initialized invalid number of "
            "default verifiers, when signature verification env property is "
            "disabled")

        verifier = default_verifiers[0]
        self.assertIsInstance(
            verifier, TimestampVerifier,
            "Webservice skill handler initialized invalid default verifier, "
            "when request signature verification env property is set to false")

    def test_webservice_skill_handler_dispatch_serialization_failure_throw_exc(
            self):
        self.mock_serializer.deserialize.side_effect = AskSdkException(
            "test deserialization exception")
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_signature=False,
            verify_timestamp=False, verifiers=[self.mock_verifier])

        with self.assertRaises(AskSdkException) as exc:
            test_webservice_skill_handler.verify_request_and_dispatch(
                http_request_headers=None, http_request_body=None)

        self.assertIn(
            "test deserialization exception", str(exc.exception),
            "Webservice skill handler didn't raise deserialization exception "
            "during skill dispatch")

        self.assertFalse(
            self.mock_verifier.verify.called,
            "Webservice skill handler called verifier verify when request "
            "deserialization failed")

        self.assertFalse(
            self.mock_skill.invoke.called,
            "Webservice skill handler called skill invoke when request "
            "verification failed")

    def test_webservice_skill_handler_dispatch_verification_failure_throw_exc(
            self):
        self.mock_verifier.verify.side_effect = VerificationException(
            "test verification exception")
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_signature=False,
            verify_timestamp=False, verifiers=[self.mock_verifier])

        with self.assertRaises(VerificationException) as exc:
            test_webservice_skill_handler.verify_request_and_dispatch(
                http_request_headers=None, http_request_body=None)

        self.assertIn(
            "test verification exception", str(exc.exception),
            "Webservice skill handler didn't raise verification exception "
            "during skill dispatch")

        self.assertFalse(
            self.mock_skill.invoke.called,
            "Webservice skill handler called skill invoke when request "
            "verification failed")

    def test_webservice_skill_handler_dispatch_failure_throw_exc(self):
        self.mock_skill.invoke.side_effect = AskSdkException(
            "test skill invocation exception")
        test_webservice_skill_handler = WebserviceSkillHandler(
            skill=self.mock_skill, verify_signature=False,
            verify_timestamp=False, verifiers=[self.mock_verifier])

        with self.assertRaises(AskSdkException) as exc:
            test_webservice_skill_handler.verify_request_and_dispatch(
                http_request_headers=None, http_request_body=None)

        self.assertIn(
            "test skill invocation exception", str(exc.exception),
            "Webservice skill handler didn't raise invocation exception "
            "during skill dispatch")

    def test_webservice_skill_handler_dispatch_runs_verification_skill_invoke(
            self):
        try:
            test_webservice_skill_handler = WebserviceSkillHandler(
                skill=self.mock_skill, verify_signature=False,
                verify_timestamp=False, verifiers=[self.mock_verifier])
            test_webservice_skill_handler.verify_request_and_dispatch(
                http_request_headers=None, http_request_body=None)
        except:
            self.fail(
                "Webservice skill handler failed request verification "
                "and request dispatch for a valid input request")

