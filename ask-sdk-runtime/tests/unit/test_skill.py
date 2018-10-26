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

from ask_sdk_runtime.skill import (
    RuntimeConfiguration, AbstractSkill, RuntimeConfigurationBuilder)
from ask_sdk_runtime.dispatch_components import (
    GenericHandlerAdapter, GenericRequestMapper, GenericRequestHandlerChain,
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_runtime.exceptions import AskSdkException, RuntimeConfigException

try:
    import mock
except ImportError:
    from unittest import mock


class TestRuntimeConfiguration(unittest.TestCase):
    def test_no_mappers_adapters_init(self):
        test_skill_config = RuntimeConfiguration(
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


class TestRuntimeConfigurationBuilder(unittest.TestCase):
    def setUp(self):
        self.rcb = RuntimeConfigurationBuilder()

    def test_add_null_request_handler_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_request_handler(request_handler=None)

        assert "Valid Request Handler instance to be provided" in str(
            exc.exception), (
            "Add Request Handler method didn't throw exception when a null "
            "request handler is added")

    def test_add_invalid_request_handler_throw_error(self):
        invalid_request_handler = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_request_handler(
                request_handler=invalid_request_handler)

        assert "Input should be a RequestHandler instance" in str(
            exc.exception), (
            "Add Request Handler method didn't throw exception when an "
            "invalid request handler is added")

    def test_add_valid_request_handler(self):
        mock_request_handler = mock.MagicMock(
            spec=AbstractRequestHandler)

        self.rcb.add_request_handler(request_handler=mock_request_handler)

        assert (self.rcb.request_handler_chains[0].request_handler
                == mock_request_handler), (
            "Add Request Handler method didn't add valid request handler to "
            "Skill Builder Request Handlers list")

    def test_add_null_exception_handler_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_exception_handler(exception_handler=None)

        assert "Valid Exception Handler instance to be provided" in str(
            exc.exception), (
            "Add Exception Handler method didn't throw exception when a null "
            "exception handler is added")

    def test_add_invalid_exception_handler_throw_error(self):
        invalid_exception_handler = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_exception_handler(
                exception_handler=invalid_exception_handler)

        assert "Input should be an ExceptionHandler instance" in str(
            exc.exception), (
            "Add Exception Handler method didn't throw exception when an "
            "invalid exception handler is added")

    def test_add_valid_exception_handler(self):
        mock_exception_handler = mock.MagicMock(spec=AbstractExceptionHandler)

        self.rcb.add_exception_handler(exception_handler=mock_exception_handler)

        assert self.rcb.exception_handlers[0] == mock_exception_handler, (
            "Add Exception Handler method didn't add valid exception handler "
            "to Skill Builder Exception Handlers list")

    def test_add_null_global_request_interceptor_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_global_request_interceptor(request_interceptor=None)

        assert "Valid Request Interceptor instance to be provided" in str(
            exc.exception), (
            "Add Global Request Interceptor method didn't throw exception "
            "when a null request interceptor is added")

    def test_add_invalid_global_request_interceptor_throw_error(self):
        invalid_request_interceptor = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_global_request_interceptor(
                request_interceptor=invalid_request_interceptor)

        assert "Input should be a RequestInterceptor instance" in str(
            exc.exception), (
            "Add Global Request Interceptor method didn't throw exception "
            "when an invalid request interceptor is added")

    def test_add_valid_global_request_interceptor(self):
        mock_request_interceptor = mock.MagicMock(
            spec=AbstractRequestInterceptor)

        self.rcb.add_global_request_interceptor(
            request_interceptor=mock_request_interceptor)

        assert self.rcb.global_request_interceptors[0] == \
               mock_request_interceptor, (
            "Add Global Request Interceptor method didn't add valid request "
            "interceptor to Skill Builder "
            "Request Interceptors list")

    def test_add_null_global_response_interceptor_throw_error(self):
        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_global_response_interceptor(response_interceptor=None)

        assert "Valid Response Interceptor instance to be provided" in str(
            exc.exception), (
            "Add Global Response Interceptor method didn't throw exception "
            "when a null response interceptor is added")

    def test_add_invalid_global_response_interceptor_throw_error(self):
        invalid_response_interceptor = mock.Mock()

        with self.assertRaises(RuntimeConfigException) as exc:
            self.rcb.add_global_response_interceptor(
                response_interceptor=invalid_response_interceptor)

        assert "Input should be a ResponseInterceptor instance" in str(
            exc.exception), (
            "Add Global Response Interceptor method didn't throw exception "
            "when an invalid response interceptor "
            "is added")

    def test_add_valid_global_response_interceptor(self):
        mock_response_interceptor = mock.MagicMock(
            spec=AbstractResponseInterceptor)

        self.rcb.add_global_response_interceptor(
            response_interceptor=mock_response_interceptor)

        assert (self.rcb.global_response_interceptors[0] ==
                mock_response_interceptor), (
            "Add Global Response Interceptor method didn't add valid response "
            "interceptor to Skill Builder "
            "Response Interceptors list")
