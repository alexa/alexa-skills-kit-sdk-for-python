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
import inspect

from ask_sdk_model import Response
from ask_sdk_runtime.dispatch_components import (
    GenericHandlerAdapter, GenericExceptionMapper)

from ask_sdk_core.skill import CustomSkill
from ask_sdk_core.skill_builder import SkillBuilder, CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.exceptions import SkillBuilderException
from ask_sdk_core.__version__ import __version__
from ask_sdk_core.utils import RESPONSE_FORMAT_VERSION, user_agent_info

try:
    import mock
except ImportError:
    from unittest import mock


class TestSkillBuilder(unittest.TestCase):
    def setUp(self):
        self.sb = SkillBuilder()

    def test_skill_configuration_getter_no_registered_components(self):
        actual_config = self.sb.skill_configuration

        assert actual_config.request_mappers is not None, (
            "Skill Configuration getter in Skill Builder didn't set request "
            "mappers correctly")
        assert actual_config.request_mappers[0].request_handler_chains is not None, (
            "Skill Configuration getter in Skill Builder didn't set handler "
            "chains in request mappers correctly")
        assert len(actual_config.request_mappers[0].request_handler_chains) == 0, (
            "Skill Configuration getter in Skill Builder added invalid "
            "handler in handler chain, "
            "when no request handlers are registered")
        assert actual_config.handler_adapters is not None, (
            "Skill Configuration getter in Skill Builder didn't set handler "
            "adapters correctly")
        assert isinstance(
            actual_config.handler_adapters[0], GenericHandlerAdapter), (
            "Skill Configuration getter in Skill Builder didn't set default "
            "handler adapter")
        assert isinstance(
            actual_config.exception_mapper, GenericExceptionMapper), (
            "Skill Configuration getter in Skill Builder created invalid "
            "exception mapper, "
            "when no exception handlers are registered")
        assert len(actual_config.exception_mapper.exception_handlers) == 0, (
            "Skill Configuration getter in Skill Builder created invalid "
            "exception handlers in exception mapper, "
            "when no exception handlers are registered")
        assert actual_config.request_interceptors == [], (
            "Skill Configuration getter in Skill Builder created invalid "
            "request interceptors, "
            "when no global request interceptors are registered")
        assert actual_config.response_interceptors == [], (
            "Skill Configuration getter in Skill Builder created invalid "
            "response interceptors, "
            "when no global response interceptors are registered")
        assert actual_config.custom_user_agent is None, (
            "Skill Configuration getter in Skill Builder set invalid custom "
            "user agent")
        assert actual_config.skill_id is None, (
            "Skill Configuration getter in Skill Builder set invalid skill id")

    def test_skill_configuration_getter_handlers_registered(self):
        mock_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        self.sb.add_request_handler(request_handler=mock_request_handler)

        mock_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)
        self.sb.add_exception_handler(exception_handler=mock_exception_handler)

        actual_config = self.sb.skill_configuration

        assert actual_config.request_mappers is not None, (
            "Skill Configuration getter in Skill Builder didn't set request "
            "mappers correctly")
        assert actual_config.request_mappers[0].request_handler_chains is not None, (
            "Skill Configuration getter in Skill Builder didn't set handler "
            "chains in request mappers correctly")
        assert len(actual_config.request_mappers[0].request_handler_chains) == 1, (
            "Skill Configuration getter in Skill Builder didn't add valid "
            "handler in handler chain, "
            "when request handlers are registered")
        assert actual_config.request_mappers[0].request_handler_chains[0].request_handler == mock_request_handler, (
            "Skill Configuration getter in Skill Builder added invalid "
            "handler in handler chain, "
            "when request handlers are registered")

        assert actual_config.exception_mapper is not None, (
            "Skill Configuration getter in Skill Builder didn't create "
            "exception mapper, "
            "when exception handlers are registered")
        assert len(actual_config.exception_mapper.exception_handlers) == 1, (
            "Skill Configuration getter in Skill Builder added additional "
            "exception handlers than the registered ones "
            "in exception mapper")
        assert actual_config.exception_mapper.exception_handlers[0] == mock_exception_handler, (
            "Skill Configuration getter in Skill Builder added invalid "
            "handler in exception mapper, "
            "when exception handlers are registered")

    def test_create_skill(self):
        mock_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        self.sb.add_request_handler(request_handler=mock_request_handler)

        mock_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)
        self.sb.add_exception_handler(exception_handler=mock_exception_handler)

        actual_skill = self.sb.create()
        expected_skill = CustomSkill(self.sb.skill_configuration)

        assert actual_skill.request_dispatcher.request_mappers[0].request_handler_chains[0].request_handler == \
            expected_skill.request_dispatcher.request_mappers[0].request_handler_chains[0].request_handler, (
            "Skill Builder created skill with incorrect request handlers when "
            "using create method")

        assert actual_skill.request_dispatcher.exception_mapper.exception_handlers[0] == \
            expected_skill.request_dispatcher.exception_mapper.exception_handlers[0], (
            "Skill Builder created skill with incorrect exception handlers "
            "when using create method")

    def test_lambda_handler_creation(self):
        handler_func = self.sb.lambda_handler()
        assert callable(handler_func), "Skill Builder Lambda Handler " \
                                       "function returned an invalid object"

        actual_arg_spec = inspect.getargspec(handler_func)
        assert len(actual_arg_spec.args) == 2, (
            "Skill Builder Lambda Handler function created a handler of "
            "different signature than AWS Lambda")
        assert "event" in actual_arg_spec.args, (
            "Skill Builder Lambda Handler function created a handler without "
            "named parameter event")
        assert "context" in actual_arg_spec.args, (
            "Skill Builder Lambda Handler function created a handler without "
            "named parameter context")

    def test_lambda_handler_invocation(self):
        mock_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        mock_request_handler.can_handle.return_value = True
        mock_response = Response()
        mock_response.output_speech = "test output speech"
        mock_request_handler.handle.return_value = mock_response
        self.sb.add_request_handler(request_handler=mock_request_handler)

        mock_request_envelope_payload = {
            "context": {
                "System": {
                    "application": {
                        "applicationId": "test"
                    }
                }
            }
        }

        self.sb.skill_id = "test"
        lambda_handler = self.sb.lambda_handler()

        response_envelope = lambda_handler(
            event=mock_request_envelope_payload, context=None)

        assert response_envelope["version"] == RESPONSE_FORMAT_VERSION, (
            "Response Envelope from lambda handler invocation has version "
            "different than expected")
        assert response_envelope["userAgent"] == user_agent_info(
            sdk_version=__version__,
            custom_user_agent=None), (
            "Response Envelope from lambda handler invocation has user agent "
            "info different than expected")
        assert response_envelope["response"]["outputSpeech"] == "test output speech", (
            "Response Envelope from lambda handler invocation has incorrect "
            "response than built by skill")


class TestCustomSkillBuilder(unittest.TestCase):
    def test_custom_persistence_adapter_default_null(self):
        test_custom_skill_builder = CustomSkillBuilder()

        actual_skill_config = test_custom_skill_builder.skill_configuration

        assert actual_skill_config.persistence_adapter is None, (
            "Custom Skill Builder didn't set the default persistence adapter "
            "as None")

    def test_custom_persistence_adapter_used(self):
        mock_adapter = mock.Mock()
        test_custom_skill_builder = CustomSkillBuilder(
            persistence_adapter=mock_adapter)

        actual_skill_config = test_custom_skill_builder.skill_configuration

        assert actual_skill_config.persistence_adapter == mock_adapter, (
            "Custom Skill Builder didn't set the persistence adapter provided")

    def test_custom_api_client_default_null(self):
        test_custom_skill_builder = CustomSkillBuilder()

        actual_skill_config = test_custom_skill_builder.skill_configuration

        assert actual_skill_config.api_client is None, (
            "Custom Skill Builder didn't set the default api client "
            "as None")

    def test_custom_api_client_used(self):
        mock_api_client = mock.Mock()
        test_custom_skill_builder = CustomSkillBuilder(
            api_client=mock_api_client)

        actual_skill_config = test_custom_skill_builder.skill_configuration

        assert actual_skill_config.api_client == mock_api_client, (
            "Custom Skill Builder didn't set the api client provided")
