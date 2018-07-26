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

from ask_sdk_core.handler_input import HandlerInput

try:
    import mock
except ImportError:
    from unittest import mock


class TestHandlerInput(unittest.TestCase):
    def test_error_thrown_when_service_client_factory_getter_called_without_setting(self):
        test_input = HandlerInput(request_envelope=None)
        with self.assertRaises(ValueError) as exc:
            test_client_factory = test_input.service_client_factory

        assert "Attempting to use service client factory with no configured API client" in str(exc.exception), (
            "Handler Input didn't raise Value Error when service client "
            "factory is not set and a get is called")

    def test_no_error_thrown_when_service_client_factory_getter_called_after_setting(self):
        test_input = HandlerInput(
            request_envelope=None, service_client_factory=mock.Mock())
        test_client_factory = test_input.service_client_factory

        assert isinstance(test_client_factory, mock.Mock), (
            "Handler Input service client factory getter returned incorrect "
            "value for client factory after setter")
