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

from ask_sdk_runtime.skill_builder import AbstractSkillBuilder
from ask_sdk_runtime.dispatch_components import (
    GenericHandlerAdapter, GenericRequestMapper, GenericRequestHandlerChain,
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor,
    GenericExceptionMapper)
from ask_sdk_runtime.exceptions import (
    RuntimeConfigException, SkillBuilderException)

try:
    import mock
except ImportError:
    from unittest import mock


class CustomSkillBuilder(AbstractSkillBuilder):
    # Implementing a mock skill builder, for Py2.7 tests
    def create(self):
        return None


class TestSkillBuilder(unittest.TestCase):
    def setUp(self):
        self.sb = CustomSkillBuilder()

    def test_add_null_request_handler_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_request_handler(request_handler=None)

        assert "Valid Request Handler instance to be provided" in str(
            exc.exception), (
            "Add Request Handler method didn't throw exception when a null "
            "request handler is added")

    def test_add_invalid_request_handler_throw_error(self):
        invalid_request_handler = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_request_handler(
                request_handler=invalid_request_handler)

        assert "Input should be a RequestHandler instance" in str(
            exc.exception), (
            "Add Request Handler method didn't throw exception when an "
            "invalid request handler is added")

    def test_add_valid_request_handler(self):
        mock_request_handler = mock.MagicMock(spec=AbstractRequestHandler)

        self.sb.add_request_handler(request_handler=mock_request_handler)

        options = self.sb.runtime_configuration_builder
        assert options.request_handler_chains[0].request_handler == mock_request_handler, (
            "Add Request Handler method didn't add valid request handler to "
            "Skill Builder Request Handlers list")

    def test_add_null_exception_handler_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_exception_handler(exception_handler=None)

        assert "Valid Exception Handler instance to be provided" in str(
            exc.exception), (
            "Add Exception Handler method didn't throw exception when a null "
            "exception handler is added")

    def test_add_invalid_exception_handler_throw_error(self):
        invalid_exception_handler = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_exception_handler(
                exception_handler=invalid_exception_handler)

        assert "Input should be an ExceptionHandler instance" in str(
            exc.exception), (
            "Add Exception Handler method didn't throw exception when an "
            "invalid exception handler is added")

    def test_add_valid_exception_handler(self):
        mock_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)

        self.sb.add_exception_handler(exception_handler=mock_exception_handler)
        options = self.sb.runtime_configuration_builder

        assert options.exception_handlers[0] == mock_exception_handler, (
            "Add Exception Handler method didn't add valid exception handler "
            "to Skill Builder Exception Handlers list")

    def test_add_null_global_request_interceptor_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_global_request_interceptor(request_interceptor=None)

        assert "Valid Request Interceptor instance to be provided" in str(
            exc.exception), (
            "Add Global Request Interceptor method didn't throw exception "
            "when a null request interceptor is added")

    def test_add_invalid_global_request_interceptor_throw_error(self):
        invalid_request_interceptor = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_global_request_interceptor(
                request_interceptor=invalid_request_interceptor)

        assert "Input should be a RequestInterceptor instance" in str(
            exc.exception), (
            "Add Global Request Interceptor method didn't throw exception "
            "when an invalid request interceptor is added")

    def test_add_valid_global_request_interceptor(self):
        mock_request_interceptor = mock.MagicMock(
            spec=AbstractRequestInterceptor)

        self.sb.add_global_request_interceptor(
            request_interceptor=mock_request_interceptor)
        options = self.sb.runtime_configuration_builder

        assert (options.global_request_interceptors[0] ==
               mock_request_interceptor), (
            "Add Global Request Interceptor method didn't add valid request "
            "interceptor to Skill Builder "
            "Request Interceptors list")

    def test_add_null_global_response_interceptor_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_global_response_interceptor(response_interceptor=None)

        assert "Valid Response Interceptor instance to be provided" in str(
            exc.exception), (
            "Add Global Response Interceptor method didn't throw exception "
            "when a null response interceptor is added")

    def test_add_invalid_global_response_interceptor_throw_error(self):
        invalid_response_interceptor = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.sb.add_global_response_interceptor(
                response_interceptor=invalid_response_interceptor)

        assert "Input should be a ResponseInterceptor instance" in str(
            exc.exception), (
            "Add Global Response Interceptor method didn't throw exception "
            "when an invalid response interceptor "
            "is added")

    def test_add_valid_global_response_interceptor(self):
        mock_response_interceptor = mock.MagicMock(
            spec=AbstractResponseInterceptor)

        self.sb.add_global_response_interceptor(
            response_interceptor=mock_response_interceptor)
        options = self.sb.runtime_configuration_builder

        assert (options.global_response_interceptors[0] ==
               mock_response_interceptor), (
            "Add Global Response Interceptor method didn't add valid response "
            "interceptor to Skill Builder "
            "Response Interceptors list")

    def test_skill_configuration_getter_no_registered_components(self):
        actual_config = self.sb.runtime_configuration_builder.get_runtime_configuration()

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
        assert isinstance(actual_config.handler_adapters[0], GenericHandlerAdapter), (
            "Skill Configuration getter in Skill Builder didn't set default "
            "handler adapter")
        assert actual_config.exception_mapper is not None, (
            "Skill Configuration getter in Skill Builder created invalid "
            "exception mapper, "
            "when no exception handlers are registered")
        assert actual_config.request_interceptors == [], (
            "Skill Configuration getter in Skill Builder created invalid "
            "request interceptors, "
            "when no global request interceptors are registered")
        assert actual_config.response_interceptors == [], (
            "Skill Configuration getter in Skill Builder created invalid "
            "response interceptors, "
            "when no global response interceptors are registered")

    def test_skill_configuration_getter_handlers_registered(self):
        mock_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        self.sb.add_request_handler(request_handler=mock_request_handler)

        mock_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)
        self.sb.add_exception_handler(exception_handler=mock_exception_handler)

        actual_config = self.sb.runtime_configuration_builder.get_runtime_configuration()

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

    def test_request_handler_decorator_creation(self):
        request_handler_wrapper = self.sb.request_handler(can_handle_func=None)
        assert callable(request_handler_wrapper), (
            "Skill Builder Request Handler decorator returned an invalid "
            "wrapper object")

        actual_arg_spec = inspect.getargspec(request_handler_wrapper)
        assert len(actual_arg_spec.args) == 1, (
            "Skill Builder Request Handler decorator created a wrapper of "
            "different signature than expected")
        assert "handle_func" in actual_arg_spec.args, (
            "Skill Builder Request Handler decorator created a wrapper "
            "without named parameter handler_func")

    def test_request_handler_decorator_invalid_can_handle_func(self):
        request_handler_wrapper = self.sb.request_handler(
            can_handle_func=None)

        with self.assertRaises(SkillBuilderException) as exc:
            request_handler_wrapper(handle_func=None)

        assert ("can_handle_func and handle_func input parameters should "
                "be callable") in str(exc.exception), (
            "Request Handler Decorator accepted invalid can_handle_func "
            "parameter")

    def test_request_handler_decorator_invalid_handle_func(self):
        request_handler_wrapper = self.sb.request_handler(
            can_handle_func=lambda x: True)

        with self.assertRaises(SkillBuilderException) as exc:
            request_handler_wrapper(handle_func=None)

        assert ("can_handle_func and handle_func input parameters should "
                "be callable") in str(exc.exception), (
            "Request Handler Decorator was decorated on an invalid object")

    def test_request_handler_decorator_on_valid_handle_func(self):
        def test_can_handle(input):
            return True

        def test_handle(input):
            return "something"

        returned_request_handler = self.sb.request_handler(can_handle_func=test_can_handle)(
            handle_func=test_handle)

        options = self.sb.runtime_configuration_builder
        actual_request_handler_chain = options.request_handler_chains[0]
        actual_request_handler = actual_request_handler_chain.request_handler

        assert (actual_request_handler.__class__.__name__
                == "RequestHandlerTestHandle"), (
            "Request Handler decorator created Request Handler of incorrect "
            "name")
        assert actual_request_handler.can_handle(None) is True, (
            "Request Handler decorator created Request Handler with incorrect "
            "can_handle function")
        assert actual_request_handler.handle(None) == "something", (
            "Request Handler decorator created Request Handler with incorrect "
            "handle function")
        assert returned_request_handler == test_handle, (
            "Request Handler wrapper returned incorrect function"
        )

    def test_exception_handler_decorator_creation(self):
        exception_handler_wrapper = self.sb.exception_handler(
            can_handle_func=None)
        assert callable(exception_handler_wrapper), (
            "Skill Builder Exception Handler decorator returned an invalid "
            "wrapper object")

        actual_arg_spec = inspect.getargspec(exception_handler_wrapper)
        assert len(actual_arg_spec.args) == 1, (
            "Skill Builder Exception Handler decorator created a wrapper of "
            "different signature than expected")
        assert "handle_func" in actual_arg_spec.args, (
            "Skill Builder Exception Handler decorator created a wrapper "
            "without named parameter handler_func")

    def test_exception_handler_decorator_invalid_can_handle_func(self):
        exception_handler_wrapper = self.sb.exception_handler(
            can_handle_func=None)

        with self.assertRaises(SkillBuilderException) as exc:
            exception_handler_wrapper(handle_func=None)

        assert ("can_handle_func and handle_func input parameters should "
                "be callable") in str(exc.exception), (
            "Exception Handler Decorator accepted invalid can_handle_func "
            "parameter")

    def test_exception_handler_decorator_invalid_handle_func(self):
        exception_handler_wrapper = self.sb.exception_handler(
            can_handle_func=lambda x: True)

        with self.assertRaises(SkillBuilderException) as exc:
            exception_handler_wrapper(handle_func=None)

        assert ("can_handle_func and handle_func input parameters should "
                "be callable") in str(exc.exception), (
            "Exception Handler Decorator was decorated on an invalid object")

    def test_exception_handler_decorator_on_valid_handle_func(self):
        def test_can_handle(input, exc):
            return True

        def test_handle(input, exc):
            return "something"

        returned_exception_handler = self.sb.exception_handler(can_handle_func=test_can_handle)(
            handle_func=test_handle)

        options = self.sb.runtime_configuration_builder
        actual_exception_handler = options.exception_handlers[0]

        assert (actual_exception_handler.__class__.__name__
                == "ExceptionHandlerTestHandle"), (
            "Exception Handler decorator created Exception Handler of "
            "incorrect name")
        assert actual_exception_handler.can_handle(None, None) is True, (
            "Exception Handler decorator created Exception Handler with "
            "incorrect can_handle function")
        assert actual_exception_handler.handle(None, None) == "something", (
            "Exception Handler decorator created Exception Handler with "
            "incorrect handle function")
        assert returned_exception_handler == test_handle, (
            "Exception Handler wrapper returned incorrect function"
        )

    def test_global_request_interceptor_decorator_creation(self):
        request_interceptor_wrapper = self.sb.global_request_interceptor()
        assert callable(request_interceptor_wrapper), (
            "Skill Builder Global Request Interceptor decorator returned an "
            "invalid wrapper object")

        actual_arg_spec = inspect.getargspec(request_interceptor_wrapper)
        assert len(actual_arg_spec.args) == 1, (
            "Skill Builder Global Request Interceptor decorator created a "
            "wrapper of different signature than expected")
        assert "process_func" in actual_arg_spec.args, (
            "Skill Builder Global Request Interceptor decorator created a "
            "wrapper without named parameter process_func")

    def test_global_request_interceptor_decorator_invalid_process_func(self):
        request_interceptor_wrapper = self.sb.global_request_interceptor()

        with self.assertRaises(SkillBuilderException) as exc:
            request_interceptor_wrapper(process_func=None)

        assert "process_func input parameter should be callable" in str(
            exc.exception), (
            "Global Request Interceptor Decorator accepted invalid "
            "process_func parameter")

    def test_global_request_interceptor_decorator_on_valid_process_func(self):
        def test_process(input):
            return "something"

        returned_process_func = self.sb.global_request_interceptor()(process_func=test_process)

        options = self.sb.runtime_configuration_builder
        actual_global_request_interceptor = options.global_request_interceptors[0]

        assert (actual_global_request_interceptor.__class__.__name__
                == "RequestInterceptorTestProcess")
        assert actual_global_request_interceptor.process(None) == "something"
        assert returned_process_func == test_process, (
            "Request Interceptor wrapper returned incorrect function"
        )

    def test_global_response_interceptor_decorator_creation(self):
        response_interceptor_wrapper = self.sb.global_response_interceptor()
        assert callable(response_interceptor_wrapper), (
            "Skill Builder Global Request Interceptor decorator returned an "
            "invalid wrapper object")

        actual_arg_spec = inspect.getargspec(response_interceptor_wrapper)
        assert len(actual_arg_spec.args) == 1, (
            "Skill Builder Global Response Interceptor decorator created a "
            "wrapper of different signature than "
            "expected")
        assert "process_func" in actual_arg_spec.args, (
            "Skill Builder Global Response Interceptor decorator created a "
            "wrapper without named parameter "
            "process_func")

    def test_global_response_interceptor_decorator_invalid_process_func(self):
        response_interceptor_wrapper = self.sb.global_response_interceptor()

        with self.assertRaises(SkillBuilderException) as exc:
            response_interceptor_wrapper(process_func=None)

        assert "process_func input parameter should be callable" in str(
            exc.exception), (
            "Global Response Interceptor Decorator accepted invalid "
            "process_func parameter")

    def test_global_response_interceptor_decorator_on_valid_process_func(self):
        def test_process(input, response):
            return "something"

        returned_process_func = self.sb.global_response_interceptor()(process_func=test_process)

        options = self.sb.runtime_configuration_builder
        actual_global_response_interceptor = options.global_response_interceptors[0]

        assert (actual_global_response_interceptor.__class__.__name__
                == "ResponseInterceptorTestProcess")
        assert actual_global_response_interceptor.process(None, None) == (
            "something")
        assert returned_process_func == test_process, (
            "Response Interceptor wrapper returned incorrect function"
        )

