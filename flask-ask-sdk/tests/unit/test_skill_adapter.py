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
import logging

from flask_ask_sdk.skill_adapter import (
    SkillAdapter, EXTENSION_NAME,
    VERIFY_SIGNATURE_APP_CONFIG, VERIFY_TIMESTAMP_APP_CONFIG)
from ask_sdk_core.skill import CustomSkill
from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_model.response_envelope import ResponseEnvelope
from ask_sdk_webservice_support.webservice_handler import (
    WebserviceSkillHandler)
from ask_sdk_webservice_support.verifier import (
    AbstractVerifier, VerificationException)
from flask import Flask, jsonify

try:
    import mock
except ImportError:
    from unittest import mock


class TestSkillAdapter(unittest.TestCase):
    def setUp(self):
        self.mock_skill = mock.MagicMock(spec=CustomSkill)
        self.mock_skill.custom_user_agent = None
        self.skill_id = 12345
        self.test_app = Flask(__name__)

    def check_config_not_set(self, app):
        self.assertIsNone(app.config.get(VERIFY_SIGNATURE_APP_CONFIG))
        self.assertIsNone(app.config.get(VERIFY_TIMESTAMP_APP_CONFIG))

    def check_extension_mapping_not_set(self, app, ext_map=None):
        if ext_map is None:
            self.assertIsNone(app.extensions.get(EXTENSION_NAME))
        else:
            self.assertIsNone(
                app.extensions.get(EXTENSION_NAME).get(self.skill_id))

    def check_config_set(
            self, app, signature_config=True, timestamp_config=True):
        self.assertEqual(
            app.config.get(VERIFY_SIGNATURE_APP_CONFIG), signature_config,
            "init_app method didn't set default configuration value "
            "for {}".format(VERIFY_SIGNATURE_APP_CONFIG))

        self.assertEqual(
            app.config.get(VERIFY_TIMESTAMP_APP_CONFIG), timestamp_config,
            "init_app method didn't set default configuration value "
            "for {}".format(VERIFY_SIGNATURE_APP_CONFIG))

    def check_extension_mapping_set(
            self, app, other_skill_id=None, value=None):
        if other_skill_id is not None:
            self.assertEqual(
                app.extensions.get(EXTENSION_NAME).get(other_skill_id), value,
                "init_app method incorrectly instantiated extension mapping")

        self.assertIsNotNone(
            app.extensions.get(EXTENSION_NAME).get(self.skill_id),
            "init_app method didn't instantiate skill id mapping in app "
            "extensions")

    def test_invalid_skill_instance_throw_exception(self):
        with self.assertRaises(TypeError) as exc:
            SkillAdapter(skill=None, skill_id=None)

        self.assertIn(
            "Invalid skill instance provided", str(exc.exception),
            "SkillAdapter constructor didn't throw exception for "
            "invalid skill input")

    def test_init_sets_no_config_when_no_app_provided(self):
        skill_adapter = mock.MagicMock(spec=SkillAdapter)
        self.assertFalse(
            skill_adapter.init_app.called,
            "SkillAdapter constructor called init_app method even if "
            "no app was provided")

    def test_init_sets_config_when_app_provided(self):
        self.check_config_not_set(self.test_app)
        self.check_extension_mapping_not_set(self.test_app)

        SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id, app=self.test_app)
        self.check_config_set(self.test_app)
        self.check_extension_mapping_set(self.test_app)

    def test_init_app_sets_app_configurations(self):
        self.check_config_not_set(self.test_app)
        self.check_extension_mapping_not_set(self.test_app)

        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        test_skill_adapter.init_app(self.test_app)
        self.check_config_set(self.test_app)
        self.check_extension_mapping_set(self.test_app)

    def test_init_app_creates_user_agent_if_not_set(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id, app=self.test_app)

        self.assertIn("ask-webservice flask-ask-sdk",
                      self.mock_skill.custom_user_agent,
                      "SkillAdapter didn't update custom user agent "
                      "for a valid custom skill without any user agent set")

    def test_init_app_appends_user_agent_if_already_set(self):
        self.mock_skill.custom_user_agent = "test-agent"
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id, app=self.test_app)

        self.assertEqual("test-agent ask-webservice flask-ask-sdk",
                         self.mock_skill.custom_user_agent,
                         "SkillAdapter didn't update custom user agent "
                         "for a valid custom skill with a user agent set")

    def test_init_app_sets_default_config_if_not_present(self):
        self.test_app.config[VERIFY_SIGNATURE_APP_CONFIG] = False

        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        test_skill_adapter.init_app(self.test_app)
        self.check_config_set(self.test_app, signature_config=False)

    def test_init_app_sets_multiple_ext_with_skill_ids(self):
        self.test_app.extensions[EXTENSION_NAME] = {}
        self.test_app.extensions[EXTENSION_NAME]["test"] = "value"

        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        test_skill_adapter.init_app(self.test_app)
        self.check_extension_mapping_set(self.test_app, "test", "value")

    def test_request_dispatch_http_get_throw_method_not_allowed(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id, app=self.test_app)

        self.test_app.add_url_rule(
            "/", "index", test_skill_adapter.dispatch_request)

        self.test_app.testing = True
        with self.test_app.test_client() as c:
            test_response = c.get("/")

            self.assertEqual(
                test_response.status_code, 405,
                "SkillAdapter didn't raise method not allowed exception "
                "when a GET request hits the registered route")

    def test_request_dispatch_verification_failure_throw_exception(self):
        self.test_app.config[VERIFY_SIGNATURE_APP_CONFIG] = False
        self.test_app.config[VERIFY_TIMESTAMP_APP_CONFIG] = False
        self.test_app.logger.setLevel(logging.CRITICAL)

        mocked_handler = mock.MagicMock(spec=WebserviceSkillHandler)
        mocked_handler.verify_request_and_dispatch.side_effect = \
            VerificationException("test")
        with mock.patch(
                "flask_ask_sdk.skill_adapter.WebserviceSkillHandler",
                return_value=mocked_handler):
            test_skill_adapter = SkillAdapter(
                skill=self.mock_skill, skill_id=self.skill_id,
                app=self.test_app)

            self.test_app.add_url_rule(
                "/", "index", test_skill_adapter.dispatch_request,
                methods=["POST"])

            self.test_app.testing = True
            with self.test_app.test_client() as c:
                test_response = c.post(
                    "/", data={}, content_type="application/json")

                self.assertEqual(
                    test_response.status_code, 400,
                    "SkillAdapter didn't raise bad request when input "
                    "verification failed")

    def test_request_dispatch_failure_throw_exception(self):
        self.test_app.config[VERIFY_SIGNATURE_APP_CONFIG] = False
        self.test_app.config[VERIFY_TIMESTAMP_APP_CONFIG] = False
        self.test_app.logger.setLevel(logging.CRITICAL)

        mocked_handler = mock.MagicMock(spec=WebserviceSkillHandler)
        mocked_handler.verify_request_and_dispatch.side_effect = \
            AskSdkException("test")
        with mock.patch(
                "flask_ask_sdk.skill_adapter.WebserviceSkillHandler",
                return_value=mocked_handler):
            test_skill_adapter = SkillAdapter(
                skill=self.mock_skill, skill_id=self.skill_id,
                app=self.test_app)

            self.test_app.add_url_rule(
                "/", "index", test_skill_adapter.dispatch_request,
                methods=["POST"])

            self.test_app.testing = True
            with self.test_app.test_client() as c:
                test_response = c.post(
                    "/", data={}, content_type="application/json")

                self.assertEqual(
                    test_response.status_code, 500,
                    "SkillAdapter didn't raise internal error when "
                    "skill invocation failed")

    def test_request_dispatch(self):
        self.test_app.config[VERIFY_SIGNATURE_APP_CONFIG] = False
        self.test_app.config[VERIFY_TIMESTAMP_APP_CONFIG] = False

        mocked_handler = mock.MagicMock(spec=WebserviceSkillHandler)
        test_response_env = ResponseEnvelope().to_str()
        with self.test_app.app_context():
            expected_response = jsonify(test_response_env)
        mocked_handler.verify_request_and_dispatch.return_value = \
            test_response_env
        with mock.patch(
                "flask_ask_sdk.skill_adapter.WebserviceSkillHandler",
                return_value=mocked_handler):
            test_skill_adapter = SkillAdapter(
                skill=self.mock_skill, skill_id=self.skill_id,
                app=self.test_app)

            self.test_app.add_url_rule(
                "/", "index", test_skill_adapter.dispatch_request,
                methods=["POST"])

            self.test_app.testing = True
            with self.test_app.test_client() as c:
                actual_response = c.post(
                    "/", data={}, content_type="application/json")

                self.assertEqual(
                    actual_response.status_code, 200,
                    "SkillAdapter didn't return valid status code "
                    "during successful skill dispatch")
                self.assertEqual(
                    actual_response.data, expected_response.data,
                    "SkillAdapter didn't return correct response on "
                    "successful skill dispatch")

    def test_register_url_rule_no_app_throw_exception(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        with self.assertRaises(TypeError) as exc:
            test_skill_adapter.register(app=None, route="/")

        self.assertIn(
            "Expected a valid Flask instance", str(exc.exception),
            "register method didn't throw exception when no app was passed")

    def test_register_url_rule_invalid_app_throw_exception(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        with self.assertRaises(TypeError) as exc:
            test_skill_adapter.register(app="test app", route="/")

        self.assertIn(
            "Expected a valid Flask instance", str(exc.exception),
            "register method didn't throw exception when invalid app "
            "was passed")

    def test_register_url_rule_no_route_throw_exception(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        with self.assertRaises(TypeError) as exc:
            test_skill_adapter.register(app=self.test_app, route=None)

        self.assertIn(
            "Expected a valid URL rule string", str(exc.exception),
            "register method didn't throw exception when no route was passed")

    def test_register_url_rule_invalid_route_throw_exception(self):
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        with self.assertRaises(TypeError) as exc:
            test_skill_adapter.register(app=self.test_app, route=1234)

        self.assertIn(
            "Expected a valid URL rule string", str(exc.exception),
            "register method didn't throw exception when invalid route "
            "was passed")

    def test_register_url_rule(self):
        mock_app = mock.MagicMock(Flask)
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        test_skill_adapter.register(app=mock_app, route="/")

        mock_app.add_url_rule.assert_called_with(
            "/", endpoint=None, methods=['POST'],
            view_func=test_skill_adapter.dispatch_request)

    def test_register_url_rule_with_endpoint(self):
        mock_app = mock.MagicMock(Flask)
        test_skill_adapter = SkillAdapter(
            skill=self.mock_skill, skill_id=self.skill_id)

        test_skill_adapter.register(app=mock_app, route="/", endpoint="test")

        mock_app.add_url_rule.assert_called_with(
            "/", endpoint="test", methods=['POST'],
            view_func=test_skill_adapter.dispatch_request)






