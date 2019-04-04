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

from ask_sdk_runtime.dispatch import GenericRequestDispatcher
from ask_sdk_runtime.skill import RuntimeConfiguration
from ask_sdk_runtime.dispatch_components import (
    GenericRequestMapper, AbstractRequestHandler, GenericRequestHandlerChain,
    GenericHandlerAdapter, AbstractRequestInterceptor,
    AbstractResponseInterceptor, AbstractExceptionHandler, GenericExceptionMapper)
from ask_sdk_runtime.exceptions import DispatchException

try:
    import mock
except ImportError:
    from unittest import mock


class TestDispatchInput(object):
    def __init__(self, request):
        # type: (str) -> None
        self.request = request


class TestDispatchOutput(object):
    def __init__(self, response):
        # type: (str) -> None
        self.response = response


class TestRequestDispatcher(unittest.TestCase):
    def setUp(self):
        self.valid_handler_input = mock.Mock()
        self.test_dispatcher = GenericRequestDispatcher(
            options=RuntimeConfiguration(
                request_mappers=None, handler_adapters=None))

    def test_handler_input_with_no_chains_in_request_mapper(self):
        with self.assertRaises(DispatchException) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Unable to find a suitable request handler" in str(exc.exception), (
            "Dispatcher didn't throw Dispatch Exception when no chains are "
            "registered in request mappers")

    def test_handler_input_with_unsupported_chains_in_request_mapper(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = False
        test_request_handler_chain = mock.MagicMock(
            spec=GenericRequestHandlerChain)
        test_request_handler_chain.request_handler = test_request_handler
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        self.test_dispatcher.request_mappers = [test_request_mapper]
        with self.assertRaises(DispatchException) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Unable to find a suitable request handler" in str(exc.exception), (
            "Dispatcher didn't throw Dispatch Exception when no suitable "
            "chains are registered in "
            "request mappers")

    def test_handler_input_with_supported_chain_in_mapper_no_adapters(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler_chain = mock.MagicMock(
            spec=GenericRequestHandlerChain)
        test_request_handler_chain.request_handler = test_request_handler
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        self.test_dispatcher.request_mappers = [test_request_mapper]
        with self.assertRaises(DispatchException) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Unable to find a suitable request adapter" in str(
            exc.exception), (
            "Dispatcher didn't throw Dispatch Exception when no adapters are "
            "registered in "
            "dispatcher")

    def test_handler_input_with_supported_chain_in_mapper_and_unsupported_adapter(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler_chain = mock.MagicMock(
            spec=GenericRequestHandlerChain)
        test_request_handler_chain.request_handler = test_request_handler
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])
        test_adapter = mock.MagicMock(spec=GenericHandlerAdapter)
        test_adapter.supports.return_value = False

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]
        with self.assertRaises(DispatchException) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Unable to find a suitable request adapter" in str(
            exc.exception), (
            "Dispatcher didn't throw Dispatch Exception when no suitable "
            "adapters are registered in "
            "dispatcher")

    def test_handler_input_successful_execution_with_supported_chain_and_supported_adapter(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = GenericHandlerAdapter()

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]

        assert self.test_dispatcher.dispatch(
            handler_input=self.valid_handler_input) == "Test Response", (
            "Dispatcher dispatch method return invalid response when "
            "supported handler chain and "
            "supported handler adapter are found")

        test_request_handler.handle.assert_called_once_with(
            self.valid_handler_input), (
            "Dispatcher dispatch method called handle on Request Handler "
            "more than once")

    def test_handler_input_successful_local_request_interceptors_execution(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_interceptor_1 = mock.MagicMock(spec=AbstractRequestInterceptor)
        test_interceptor_2 = mock.MagicMock(spec=AbstractRequestInterceptor)

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler,
            request_interceptors=[test_interceptor_1, test_interceptor_2])
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = GenericHandlerAdapter()

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]

        self.test_dispatcher.dispatch(
            handler_input=self.valid_handler_input)

        test_interceptor_1.process.assert_called_once_with(
            handler_input=self.valid_handler_input), (
            "Dispatcher dispatch method didn't process local request "
            "interceptors before calling request handler "
            "handle")
        test_interceptor_2.process.assert_called_once_with(
            handler_input=self.valid_handler_input), (
            "Dispatcher dispatch method didn't process local request "
            "interceptors before calling request handler "
            "handle")

    def test_handler_input_successful_global_request_interceptors_execution(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_interceptor_1 = mock.MagicMock(spec=AbstractRequestInterceptor)
        test_interceptor_2 = mock.MagicMock(spec=AbstractRequestInterceptor)

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = GenericHandlerAdapter()

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]
        self.test_dispatcher.request_interceptors = [
            test_interceptor_1, test_interceptor_2]

        self.test_dispatcher.dispatch(handler_input=self.valid_handler_input)

        test_interceptor_1.process.assert_called_once_with(
            handler_input=self.valid_handler_input), (
            "Dispatcher dispatch method didn't process global request "
            "interceptors before calling dispatch request")
        test_interceptor_2.process.assert_called_once_with(
            handler_input=self.valid_handler_input), (
            "Dispatcher dispatch method didn't process global request "
            "interceptors before calling dispatch request")

    def test_handler_input_unsuccessful_global_request_interceptors_execution(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_request_interceptor_1 = mock.MagicMock(
            spec=AbstractRequestInterceptor)
        test_request_interceptor_1.process.side_effect = ValueError(
            "Test exception")
        test_request_interceptor_2 = mock.MagicMock(
            spec=AbstractRequestInterceptor)
        test_response_interceptor_1 = mock.MagicMock(
            spec=AbstractResponseInterceptor)

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = GenericHandlerAdapter()

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]
        self.test_dispatcher.request_interceptors = [
            test_request_interceptor_1, test_request_interceptor_2]
        self.test_dispatcher.response_interceptors = [
            test_response_interceptor_1]

        with self.assertRaises(ValueError) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Test exception" in str(exc.exception), (
            "Dispatcher didn't throw exception raised by global request "
            "interceptor")

        test_request_interceptor_1.process.assert_called_once_with(
            handler_input=self.valid_handler_input), (
            "Dispatcher dispatch method didn't process global request "
            "interceptors before calling dispatch request")
        test_request_interceptor_2.process.assert_not_called(), (
            "Dispatcher dispatch method processed remaining global "
            "request interceptors when one of them threw "
            "exception")
        test_request_handler.assert_not_called(), (
            "Dispatcher dispatch method processed request handler 'handle' "
            "method when one of the global request "
            "interceptors threw exception")
        test_response_interceptor_1.process.assert_not_called(), (
            "Dispatcher dispatch method processed global response "
            "interceptors when one of the global request "
            "interceptors threw exception")


    def test_handler_input_successful_local_response_interceptors_execution(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_response = mock.MagicMock(spec=TestDispatchOutput)
        test_response_before_interceptor = test_response
        test_request_handler.handle.return_value = test_response

        test_interceptor_1 = mock.MagicMock(spec=AbstractResponseInterceptor)
        test_response.interceptor = "Interceptor 1"
        test_response_from_interceptor_1 = test_response
        test_interceptor_1.process.return_value = test_response

        test_interceptor_2 = mock.MagicMock(spec=AbstractResponseInterceptor)
        test_response.interceptor = "Interceptor 2"
        test_response_from_interceptor_2 = test_response
        test_interceptor_2.process.return_value = test_response

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler,
            response_interceptors=[test_interceptor_1, test_interceptor_2])
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = GenericHandlerAdapter()

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]

        assert self.test_dispatcher.dispatch(
            handler_input=self.valid_handler_input) == test_response_from_interceptor_2, (
            "Dispatcher dispatch method returned invalid response after "
            "processing response through "
            "local response interceptors")

        test_interceptor_1.process.assert_called_once_with(
            handler_input=self.valid_handler_input,
            dispatch_output=test_response_before_interceptor), (
            "Dispatcher dispatch method didn't process local response "
            "interceptors after calling request handler "
            "handle")

        test_interceptor_2.process.assert_called_once_with(
            handler_input=self.valid_handler_input,
            dispatch_output=test_response_from_interceptor_1), (
            "Dispatcher dispatch method didn't process local response "
            "interceptors after calling request handler "
            "handle")

    def test_handler_input_successful_global_response_interceptors_execution(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_response = mock.MagicMock(spec=TestDispatchOutput)
        test_response_before_interceptor = test_response
        test_request_handler.handle.return_value = test_response

        test_interceptor_1 = mock.MagicMock(spec=AbstractResponseInterceptor)
        test_response.interceptor = "Interceptor 1"
        test_response_from_interceptor_1 = test_response
        test_interceptor_1.process.return_value = test_response

        test_interceptor_2 = mock.MagicMock(spec=AbstractResponseInterceptor)
        test_response.interceptor = "Interceptor 2"
        test_response_from_interceptor_2 = test_response
        test_interceptor_2.process.return_value = test_response

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = GenericHandlerAdapter()

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]
        self.test_dispatcher.response_interceptors = [
            test_interceptor_1, test_interceptor_2]

        assert self.test_dispatcher.dispatch(
            handler_input=self.valid_handler_input) == test_response_from_interceptor_2, (
            "Dispatcher dispatch method returned invalid response after "
            "processing response through "
            "global response interceptors")

        test_interceptor_1.process.assert_called_once_with(
            handler_input=self.valid_handler_input,
            dispatch_output=test_response_before_interceptor), (
            "Dispatcher dispatch method didn't process global request "
            "interceptors after calling dispatch request")

        test_interceptor_2.process.assert_called_once_with(
            handler_input=self.valid_handler_input,
            dispatch_output=test_response_from_interceptor_1), (
            "Dispatcher dispatch method didn't process global request "
            "interceptors after calling dispatch request")

    def test_dispatch_raise_low_level_exception_when_exception_handler_not_registered(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = mock.MagicMock(spec=GenericHandlerAdapter)
        test_adapter.supports.return_value = True
        test_adapter.execute.side_effect = Exception(
            "Test low level Exception")

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]

        with self.assertRaises(Exception) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Test low level Exception" in str(exc.exception), (
            "Dispatcher didn't throw low level exception when request "
            "dispatch throws exception and "
            "no exception handler is registered")

    def test_dispatch_raise_low_level_exception_when_no_suitable_exception_handler_registered(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = mock.MagicMock(spec=GenericHandlerAdapter)
        test_adapter.supports.return_value = True
        test_adapter.execute.side_effect = Exception(
            "Test low level Exception")

        test_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)
        test_exception_handler.can_handle.return_value = False
        test_exception_mapper = GenericExceptionMapper(
            exception_handlers=[test_exception_handler])

        self.test_dispatcher.request_mappers = [test_request_mapper]
        self.test_dispatcher.handler_adapters = [test_adapter]
        self.test_dispatcher.exception_mapper = test_exception_mapper

        with self.assertRaises(Exception) as exc:
            self.test_dispatcher.dispatch(
                handler_input=self.valid_handler_input)

        assert "Test low level Exception" in str(exc.exception), (
            "Dispatcher didn't throw low level exception when request "
            "dispatch throws exception and "
            "no suitable exception handler is registered")

    def test_dispatch_process_handled_exception_when_suitable_exception_handler_registered(self):
        test_request_handler = mock.MagicMock(spec=AbstractRequestHandler)
        test_request_handler.can_handle.return_value = True
        test_request_handler.handle.return_value = "Test Response"

        test_request_handler_chain = GenericRequestHandlerChain(
            request_handler=test_request_handler)
        test_request_mapper = GenericRequestMapper(
            request_handler_chains=[test_request_handler_chain])

        test_adapter = mock.MagicMock(spec=GenericHandlerAdapter)
        test_adapter.supports.return_value = True
        test_adapter.execute.side_effect = DispatchException(
            "Custom dispatch exception")

        test_exception_handler_1 = mock.MagicMock(
            spec=AbstractExceptionHandler)
        test_exception_handler_1.can_handle.return_value = False
        test_exception_handler_2 = mock.MagicMock(
            spec=AbstractExceptionHandler)
        test_exception_handler_2.can_handle.return_value = True
        test_exception_handler_2.handle.return_value = "Custom exception " \
                                                       "handler response"

        options = RuntimeConfiguration(
            request_mappers=[test_request_mapper],
            handler_adapters=[test_adapter],
            exception_mapper=GenericExceptionMapper(
                exception_handlers=[test_exception_handler_1,
                                    test_exception_handler_2])
        )
        self.test_dispatcher = GenericRequestDispatcher(options=options)

        assert self.test_dispatcher.dispatch(
            handler_input=self.valid_handler_input) == "Custom exception handler response", (
            "Dispatcher didn't handle exception when a suitable exception handler is registered")

        test_exception_handler_1.handle.assert_not_called(), (
            "Incorrect Exception Handler called when handling custom "
            "exception")
        test_exception_handler_2.handle.assert_called_once(), (
            "Suitable exception handler didn't handle custom exception")
