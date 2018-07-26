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

from ask_sdk_model.request_envelope import RequestEnvelope
from ask_sdk_model.intent_request import IntentRequest
from ask_sdk_model.events.skillevents.skill_enabled_request import (
    SkillEnabledRequest)

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    RequestMapper, RequestHandlerChain, AbstractRequestHandler,
    RequestHandlerChain, AbstractRequestInterceptor,
    AbstractResponseInterceptor, HandlerAdapter, AbstractExceptionHandler,
    ExceptionMapper)
from ask_sdk_core.dispatch_components.request_components import (
    GenericRequestHandlerChain)
from ask_sdk_core.exceptions import DispatchException

try:
    import mock
except ImportError:
    from unittest import mock


class TestDefaultRequestMapper(unittest.TestCase):
    def test_default_request_mapper_initialization_with_null_handler_chains(self):
        test_request_mapper = RequestMapper(request_handler_chains=None)

        assert test_request_mapper.request_handler_chains == [], (
            "Request Mapper didn't initialize empty request handler chains "
            "instance variable on initialization")

    def test_default_request_mapper_initialization_with_chain_containing_null_throw_error(self):
        with self.assertRaises(DispatchException) as exc:
            test_request_mapper = RequestMapper(request_handler_chains=[None])

        assert "Request Handler Chain is not a RequestHandlerChain instance" in str(exc.exception), (
            "Request Mapper didn't throw error during initialization when a "
            "Null Handler Chain is passed")

    def test_default_request_mapper_initialization_with_chain_containing_invalid_type_throw_error(self):
        test_request_handler_chain = mock.Mock()
        with self.assertRaises(DispatchException) as exc:
            test_request_mapper = RequestMapper(
                request_handler_chains=[test_request_handler_chain])

        assert "Request Handler Chain is not a RequestHandlerChain instance" in str(exc.exception), (
            "Request Mapper didn't throw error during initialization when an "
            "invalid Handler Chain is passed")

    def test_default_request_mapper_initialization_with_chain_containing_valid_type(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler_chain = RequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = RequestMapper(
            request_handler_chains=[test_request_handler_chain])

        assert test_request_mapper.request_handler_chains == [test_request_handler_chain], (
            "Request Mapper initialization throws exception when a valid "
            "Handler Chain is provided in the "
            "handler chains list")

    def test_no_handler_registered_for_intent_request(self):
        test_intent_request = mock.MagicMock(spec=IntentRequest)
        test_request_envelope = mock.MagicMock(spec=RequestEnvelope)
        test_request_envelope.request = test_intent_request
        test_handler_input = HandlerInput(
            request_envelope=test_request_envelope)

        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = False
        test_request_handler_chain = RequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = RequestMapper(
            request_handler_chains=[test_request_handler_chain])

        assert test_request_mapper.get_request_handler_chain(
            test_handler_input) is None, (
            "get_request_handler_chain in Request Mapper found an unsupported "
            "request handler chain for "
            "intent request")

    def test_no_handler_registered_for_event_request(self):
        test_event_request = mock.MagicMock(spec=SkillEnabledRequest)
        test_request_envelope = mock.MagicMock(spec=RequestEnvelope)
        test_request_envelope.request = test_event_request
        test_handler_input = HandlerInput(
            request_envelope=test_request_envelope)

        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = False
        test_request_handler_chain = RequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = RequestMapper(
            request_handler_chains=[test_request_handler_chain])

        assert test_request_mapper.get_request_handler_chain(test_handler_input) is None, (
            "get_request_handler_chain in Request Mapper found an unsupported "
            "request handler chain for "
            "event request")

    def test_get_handler_chain_registered_for_intent_request(self):
        test_intent_request = mock.MagicMock(spec=IntentRequest)
        test_request_envelope = mock.MagicMock(spec=RequestEnvelope)
        test_request_envelope.request = test_intent_request
        test_handler_input = HandlerInput(
            request_envelope=test_request_envelope)

        test_intent_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_intent_handler.can_handle.return_value = True
        test_intent_request_handler_chain = RequestHandlerChain(
            request_handler=test_intent_handler)

        test_event_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_event_handler.can_handle.return_value = False
        test_event_request_handler_chain = RequestHandlerChain(
            request_handler=test_event_handler)

        test_request_mapper = RequestMapper(
            request_handler_chains=[test_event_request_handler_chain,
                                    test_intent_request_handler_chain])

        assert test_request_mapper.get_request_handler_chain(
            test_handler_input).request_handler == test_intent_handler, (
            "get_request_handler_chain in Request Mapper found incorrect "
            "request handler chain for "
            "intent request")

    def test_get_handler_chain_registered_for_event_request(self):
        test_intent_request = mock.MagicMock(spec=IntentRequest)
        test_request_envelope = mock.MagicMock(spec=RequestEnvelope)
        test_request_envelope.request = test_intent_request
        test_handler_input = HandlerInput(
            request_envelope=test_request_envelope)

        test_intent_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_intent_handler.can_handle.return_value = False
        test_intent_request_handler_chain = RequestHandlerChain(
            request_handler=test_intent_handler)

        test_event_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_event_handler.can_handle.return_value = True
        test_event_request_handler_chain = RequestHandlerChain(
            request_handler=test_event_handler)

        test_request_mapper = RequestMapper(
            request_handler_chains=[
                test_event_request_handler_chain,
                test_intent_request_handler_chain])

        assert test_request_mapper.get_request_handler_chain(
            test_handler_input).request_handler == test_event_handler, (
            "get_request_handler_chain in Request Mapper found incorrect "
            "request handler chain for "
            "intent request")

    def test_add_request_handler_chain_for_valid_chain_type(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler_chain = RequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = RequestMapper(
            request_handler_chains=None)

        test_request_mapper.add_request_handler_chain(
            test_request_handler_chain)

        assert test_request_mapper.request_handler_chains == [
            test_request_handler_chain], (
            "Default Request Mapper throws exception when a valid Handler "
            "Chain is provided in the "
            "add_request_handler_chain method")

    def test_add_request_handler_chain_throw_error_for_invalid_chain_type(self):
        test_request_handler_chain = mock.Mock()
        test_request_mapper = RequestMapper(request_handler_chains=None)

        with self.assertRaises(DispatchException) as exc:
            test_request_mapper.add_request_handler_chain(
                test_request_handler_chain)

        assert "Request Handler Chain is not a RequestHandlerChain instance" in str(exc.exception), (
            "Request Mapper didn't throw error during "
            "add_request_handler_chain method call when "
            "an invalid Handler Chain is passed")

    def test_add_request_handler_chain_throw_error_for_null_chain(self):
        test_request_mapper = RequestMapper(request_handler_chains=None)

        with self.assertRaises(DispatchException) as exc:
            test_request_mapper.add_request_handler_chain(None)

        assert "Request Handler Chain is not a RequestHandlerChain instance" in str(exc.exception), (
            "Request Mapper didn't throw error during "
            "add_request_handler_chain method call when "
            "a Null Handler Chain is passed")


class TestGenericRequestHandlerChain(unittest.TestCase):
    def test_generic_handler_chain_with_null_request_handler_throws_error(self):
        with self.assertRaises(DispatchException) as exc:
            test_handler_chain = GenericRequestHandlerChain(
                request_handler=None)

        assert "No Request Handler provided" in str(exc.exception), (
            "Generic Request Handler Chain didn't raise exception when no "
            "request handler is provided during "
            "instantiation")

    def test_generic_handler_chain_instantiate_request_interceptors(self):
        test_handler = mock.Mock()
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler)

        assert test_handler_chain.request_interceptors == [], (
            "Generic Request Handler Chain didn't instantiate empty list of "
            "request interceptors when no "
            "request interceptors are provided during instantiation")

    def test_generic_handler_chain_instantiate_response_interceptors(self):
        test_handler = mock.Mock()
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler)

        assert test_handler_chain.response_interceptors == [], (
            "Generic Request Handler Chain didn't instantiate empty list of "
            "response interceptors when no "
            "response interceptors are provided during instantiation")

    def test_generic_handler_chain_add_request_interceptors_to_empty_list(self):
        test_handler = mock.Mock()
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler)
        test_request_interceptor = mock.Mock()
        test_handler_chain.add_request_interceptor(
            interceptor=test_request_interceptor)

        assert test_handler_chain.request_interceptors == [test_request_interceptor], (
            "Generic Request Handler Chain didn't add interceptor to list of "
            "request interceptors when no "
            "request interceptors are provided during instantiation")

    def test_generic_handler_chain_add_request_interceptors_to_non_empty_list(self):
        test_handler = mock.Mock()
        test_interceptor_1 = mock.MagicMock(spec=AbstractRequestInterceptor)
        test_interceptors = [test_interceptor_1]
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler,
            request_interceptors=test_interceptors)
        test_request_interceptor = mock.MagicMock(
            spec=AbstractRequestInterceptor)
        test_handler_chain.add_request_interceptor(
            interceptor=test_request_interceptor)

        assert test_handler_chain.request_interceptors == [
            test_interceptor_1, test_request_interceptor], (
            "Generic Request Handler Chain didn't add interceptor to list of "
            "request interceptors when "
            "request interceptors are provided during instantiation")

    def test_generic_handler_chain_add_response_interceptors_to_empty_list(self):
        test_handler = mock.Mock()
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler)
        test_response_interceptor = mock.Mock()
        test_handler_chain.add_response_interceptor(
            interceptor=test_response_interceptor)

        assert test_handler_chain.response_interceptors == [test_response_interceptor], (
            "Generic Request Handler Chain didn't add interceptor to list of "
            "response interceptors when no "
            "response interceptors are provided during instantiation")

    def test_generic_handler_chain_add_response_interceptors_to_non_empty_list(self):
        test_handler = mock.Mock()
        test_interceptor_1 = mock.MagicMock(spec=AbstractResponseInterceptor)
        test_interceptors = [test_interceptor_1]
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler,
            response_interceptors=test_interceptors)
        test_response_interceptor = mock.MagicMock(
            spec=AbstractResponseInterceptor)
        test_handler_chain.add_response_interceptor(
            interceptor=test_response_interceptor)

        assert test_handler_chain.response_interceptors == [
            test_interceptor_1, test_response_interceptor], (
            "Generic Request Handler Chain didn't add interceptor to list of "
            "response interceptors when "
            "response interceptors are provided during instantiation")


class TestDefaultRequestHandlerChain(unittest.TestCase):
    def test_default_handler_chain_with_null_request_handler_throws_error(self):
        with self.assertRaises(DispatchException) as exc:
            test_handler_chain = RequestHandlerChain(request_handler=None)

        assert "Invalid Request Handler provided. Expected Request Handler instance" in str(exc.exception), (
            "Default Request Handler Chain didn't raise exception when no "
            "request handler is provided during "
            "instantiation")

    def test_default_handler_chain_with_invalid_request_handler_throws_error(self):
        test_handler = mock.Mock()
        with self.assertRaises(DispatchException) as exc:
            test_handler_chain = RequestHandlerChain(
                request_handler=test_handler)

        assert "Invalid Request Handler provided. Expected Request Handler instance" in str(exc.exception), (
            "Default Request Handler Chain didn't raise exception when "
            "invalid request handler is provided during "
            "instantiation")

    def test_default_handler_chain_with_invalid_request_handler_in_setter_throws_error(self):
        test_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_handler_chain = RequestHandlerChain(request_handler=test_handler)

        test_invalid_handler = mock.Mock()

        with self.assertRaises(DispatchException) as exc:
            test_handler_chain.request_handler = test_invalid_handler

        assert "Invalid Request Handler provided. Expected Request Handler instance" in str(exc.exception), (
            "Default Request Handler Chain didn't raise exception when "
            "invalid request handler is provided during "
            "instantiation")

    def test_generic_handler_chain_instantiate_call_parent_instantiation(self):
        test_handler = mock.Mock()
        test_handler_chain = GenericRequestHandlerChain(
            request_handler=test_handler)

        assert test_handler_chain.request_interceptors == [] and test_handler_chain.response_interceptors == [], (
            "Default Request Handler Chain didn't call parent instantiation "
            "method during init")


class TestDefaultHandlerAdapter(unittest.TestCase):
    def setUp(self):
        self.test_handler_adapter = HandlerAdapter()

    def test_adapter_supports_valid_handler(self):
        test_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_handler.can_handle.return_value = True

        assert self.test_handler_adapter.supports(test_handler), \
            "Handler Adapter supports method returns False for supported " \
            "Request Handler implementation"

    def test_adapter_doesnt_supports_invalid_handler(self):
        test_handler = mock.Mock()

        assert not self.test_handler_adapter.supports(test_handler), \
            "Handler Adapter supports method returns True for unsupported " \
            "Request Handler implementation"

    def test_adapter_executes_valid_handler(self):
        test_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_handler.handle.return_value = "Test Response"
        test_input = mock.MagicMock(spec=HandlerInput)

        assert self.test_handler_adapter.execute(
            handler=test_handler, handler_input=test_input) == "Test Response", (
            "Handler Adapter executes method returns unexpected response "
            "output for supported Request Handler "
            "implementation")


class TestDefaultExceptionMapper(unittest.TestCase):
    def test_exception_mapper_with_null_input(self):
        test_exception_mapper = ExceptionMapper(exception_handlers=None)

        assert test_exception_mapper.exception_handlers == [], (
            "Exception Mapper instantiated empty list of exceptions handlers "
            "when no input provided")

    def test_exception_mapper_initialization_with_handler_list_containing_null_throw_error(self):
        with self.assertRaises(DispatchException) as exc:
            test_exception_mapper = ExceptionMapper(exception_handlers=[None])

        assert "Input is not an AbstractExceptionHandler instance" in str(exc.exception), (
            "Exception Mapper didn't throw error during initialization when a "
            "Null handler is passed")

    def test_exception_mapper_initialization_with_handler_list_containing_invalid_handler_throw_error(self):
        test_invalid_handler = mock.Mock()

        with self.assertRaises(DispatchException) as exc:
            test_exception_mapper = ExceptionMapper(
                exception_handlers=[test_invalid_handler])

        assert "Input is not an AbstractExceptionHandler instance" in str(exc.exception), (
            "Exception Mapper didn't throw error during initialization when "
            "an invalid handler is passed")

    def test_exception_mapper_initialization_with_handler_list_containing_valid_handler(self):
        test_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)

        test_exception_mapper = ExceptionMapper(
            exception_handlers=[test_exception_handler])

        assert test_exception_mapper.exception_handlers == [test_exception_handler], (
            "Exception Mapper initialization throws exception when a valid "
            "Handler is provided in the "
            "exception handlers list")

    def test_add_exception_handler_for_valid_handler_type(self):
        test_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)
        test_exception_mapper = ExceptionMapper(exception_handlers=None)

        test_exception_mapper.add_exception_handler(test_exception_handler)

        assert test_exception_mapper.exception_handlers == [
            test_exception_handler], (
            "Exception Mapper throws exception when a valid Exception Handler "
            "is provided in the "
            "add_handler method")

    def test_add_request_handler_chain_throw_error_for_invalid_chain_type(self):
        test_exception_handler = mock.Mock()
        test_exception_mapper = ExceptionMapper(exception_handlers=None)

        with self.assertRaises(DispatchException) as exc:
            test_exception_mapper.add_exception_handler(test_exception_handler)

        assert "Input is not an AbstractExceptionHandler instance" in str(exc.exception), (
            "Exception Mapper didn't throw error during add_exception_handler "
            "method call when "
            "an invalid Exception Handler is passed")

    def test_add_request_handler_chain_throw_error_for_null_chain(self):
        test_exception_mapper = ExceptionMapper(exception_handlers=None)

        with self.assertRaises(DispatchException) as exc:
            test_exception_mapper.add_exception_handler(None)

        assert "Input is not an AbstractExceptionHandler instance" in str(exc.exception), (
            "Exception Mapper didn't throw error during add_exception_handler "
            "method call when "
            "an invalid Exception Handler is passed")

    def test_no_handler_registered_for_custom_exception(self):
        test_intent_request = mock.MagicMock(spec=IntentRequest)
        test_request_envelope = mock.MagicMock(spec=RequestEnvelope)
        test_request_envelope.request = test_intent_request
        test_handler_input = HandlerInput(
            request_envelope=test_request_envelope)

        test_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)
        test_exception_handler.can_handle.return_value = False
        test_exception_mapper = ExceptionMapper(
            exception_handlers=[test_exception_handler])

        test_custom_exception = DispatchException("Test Custom Exception")

        assert test_exception_mapper.get_handler(
            handler_input=test_handler_input, exception=test_custom_exception) is None, (
            "get_handler in Default Exception Mapper found an unsupported "
            "exception handler for "
            "handler input and custom exception")

    def test_get_handler_registered_for_custom_exception(self):
        test_intent_request = mock.MagicMock(spec=IntentRequest)
        test_request_envelope = mock.MagicMock(spec=RequestEnvelope)
        test_request_envelope.request = test_intent_request
        test_handler_input = HandlerInput(
            request_envelope=test_request_envelope)

        test_exception_handler_1 = mock.MagicMock(spec=AbstractExceptionHandler)
        test_exception_handler_1.can_handle.return_value = False
        test_exception_handler_2 = mock.MagicMock(spec=AbstractExceptionHandler)
        test_exception_handler_2.can_handle.return_value = True
        test_exception_mapper = ExceptionMapper(
            exception_handlers=[
                test_exception_handler_1, test_exception_handler_2])

        test_custom_exception = DispatchException("Test Custom Exception")

        assert test_exception_mapper.get_handler(
            handler_input=test_handler_input, exception=test_custom_exception) == test_exception_handler_2, (
            "get_handler in Default Exception Mapper found incorrect request "
            "exception handler for "
            "input and custom exception")