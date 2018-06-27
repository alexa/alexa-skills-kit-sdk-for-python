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
from six import PY3

from ask_sdk_model import (
    RequestEnvelope, Context, Application, Response, Session)
from ask_sdk_model.interfaces.system import SystemState

from ask_sdk_core.skill import SkillConfiguration, Skill
from ask_sdk_core.dispatch_components import (
    HandlerAdapter, RequestMapper, RequestHandlerChain)
from ask_sdk_core.exceptions import AskSdkException

if PY3:
    from unittest import mock
else:
    import mock


class TestSkillConfiguration(unittest.TestCase):
    def test_no_mappers_adapters_init(self):
        test_skill_config = SkillConfiguration(
            request_mappers=None, handler_adapters=None)
        assert test_skill_config.request_mappers == [], (
            "Empty request mappers list not set during skill configuration "
            "initialization, when nothing is provided")
        assert test_skill_config.handler_adapters == [], (
            "Empty handler adapters list not set during skill configuration "
            "initialization, when nothing is provided")
        assert test_skill_config.request_interceptors == [], (
            "Empty request interceptors list not set during skill "
            "configuration initialization, when nothing is "
            "provided")
        assert test_skill_config.response_interceptors == [], (
            "Empty response interceptors list not set during skill "
            "configuration initialization, when nothing is "
            "provided")


class TestSkill(unittest.TestCase):
    def setUp(self):
        self.mock_request_mapper = mock.MagicMock(spec=RequestMapper)
        self.mock_handler_adapter = mock.MagicMock(spec=HandlerAdapter)
        self.mock_request_handler_chain = mock.MagicMock(
            spec=RequestHandlerChain)
        self.mock_request_mapper.get_request_handler_chain.return_value = \
            self.mock_request_handler_chain

    def create_skill_config(self):
        return SkillConfiguration(
            request_mappers=[self.mock_request_mapper],
            handler_adapters=[self.mock_handler_adapter])

    def test_skill_invoke_throw_exception_when_skill_id_doesnt_match(self):
        skill_config = self.create_skill_config()
        skill_config.skill_id = "123"
        mock_request_envelope = RequestEnvelope(
            context=Context(system=SystemState(
                application=Application(application_id="test"))))
        skill = Skill(skill_configuration=skill_config)

        with self.assertRaises(AskSdkException) as exc:
            skill.invoke(request_envelope=mock_request_envelope, context=None)

        assert "Skill ID Verification failed" in str(exc.exception), (
            "Skill invocation didn't throw verification error when Skill ID "
            "doesn't match Application ID")

    def test_skill_invoke_non_empty_response_in_response_envelope(self):
        mock_request_envelope = RequestEnvelope()
        mock_response = Response()

        self.mock_handler_adapter.supports.return_value = True
        self.mock_handler_adapter.execute.return_value = mock_response

        skill_config = self.create_skill_config()
        skill = Skill(skill_configuration=skill_config)

        response_envelope = skill.invoke(
            request_envelope=mock_request_envelope, context=None)

        assert response_envelope.response == mock_response, (
            "Skill invocation returned incorrect response from "
            "request dispatch")

    def test_skill_invoke_null_response_in_response_envelope(self):
        mock_request_envelope = RequestEnvelope()

        self.mock_handler_adapter.supports.return_value = True
        self.mock_handler_adapter.execute.return_value = None

        skill_config = self.create_skill_config()
        skill = Skill(skill_configuration=skill_config)

        response_envelope = skill.invoke(
            request_envelope=mock_request_envelope, context=None)

        assert response_envelope.response is None, (
            "Skill invocation returned incorrect response from "
            "request dispatch")

    def test_skill_invoke_set_service_client_factory_if_api_client_provided(self):
        mock_request_envelope = RequestEnvelope(
            context=Context(
                system=SystemState(
                    application=Application(application_id="test"),
                    api_access_token="test_api_access_token",
                    api_endpoint="test_api_endpoint")))

        self.mock_handler_adapter.supports.return_value = True
        self.mock_handler_adapter.execute.return_value = None

        skill_config = self.create_skill_config()
        skill_config.skill_id = "test"
        skill_config.api_client = "test_api_client"
        skill = Skill(skill_configuration=skill_config)

        skill.invoke(request_envelope=mock_request_envelope, context=None)

        called_args, called_kwargs = self.mock_request_mapper.get_request_handler_chain.call_args
        test_handler_input = called_args[0]

        assert test_handler_input.service_client_factory is not None, (
            "Service Client Factory not initialized when api client is "
            "provided in skill configuration, "
            "during skill invocation")
        assert test_handler_input.service_client_factory.api_configuration.api_client == "test_api_client", (
            "Api Client value in Service Client Factory different than the "
            "one provided in skill configuration")
        assert test_handler_input.service_client_factory.api_configuration.authorization_value == \
            "test_api_access_token", ("Api Access Token value in Service "
                                      "Client Factory different than the one "
                                      "present "
                                      "in request envelope")
        assert test_handler_input.service_client_factory.api_configuration.api_endpoint == \
            "test_api_endpoint", ("Api Endpoint value in Service Client "
                                  "Factory different than the one present "
                                  "in request envelope")

    def test_skill_invoke_pass_session_attributes_to_response_envelope(self):
        mock_request_envelope = RequestEnvelope(
            context=Context(system=SystemState(
                application=Application(application_id="test"))),
            session=Session(attributes={"foo":"bar"}))

        self.mock_handler_adapter.supports.return_value = True
        self.mock_handler_adapter.execute.return_value = None

        skill_config = self.create_skill_config()
        skill_config.skill_id = "test"
        skill = Skill(skill_configuration=skill_config)

        response_envelope = skill.invoke(
            request_envelope=mock_request_envelope, context=None)

        assert response_envelope.session_attributes is not None, (
            "Session Attributes are not propagated from Request Envelope "
            "session to Response Envelope, "
            "during skill invocation")
        assert response_envelope.session_attributes["foo"] == "bar", (
            "Invalid Session Attributes propagated from Request Envelope "
            "session to Response Envelope, "
            "during skill invocation")
