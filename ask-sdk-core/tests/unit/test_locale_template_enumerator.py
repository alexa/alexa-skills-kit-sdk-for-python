# -*- coding: utf-8 -*-
#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights
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
import types
import os

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import RequestEnvelope
from ask_sdk_model.canfulfill import CanFulfillIntentRequest
from ask_sdk_core.view_resolvers.locale_template_enumerator import (
    LocaleTemplateEnumerator)


class TestLocaleTemplateEnumerator(unittest.TestCase):

    def setUp(self):
        self.test_enumerator = LocaleTemplateEnumerator()
        self.test_template_name = 'test_template'
        self.test_handler_input = HandlerInput(request_envelope=RequestEnvelope(
            request=CanFulfillIntentRequest(locale='en-GB')))

    def test_singleton_class(self):
        test_enumerator_1 = LocaleTemplateEnumerator()
        test_enumerator_2 = LocaleTemplateEnumerator()

        self.assertIs(
            test_enumerator_1, test_enumerator_2,
            "LocaleTemplateEnumerator class is not singleton"
        )

    def test_generate_combinations(self):
        test_values = [os.path.join('test_template', 'en', 'GB'),
                       os.path.join('test_template', 'en_GB'),
                       os.path.join('test_template', 'en'),
                       'test_template_en_GB',
                       'test_template_en', 'test_template']
        generator_test = self.test_enumerator.generate_combinations(
            handler_input=self.test_handler_input,
            template_name=self.test_template_name)
        self.assertIsInstance(
            generator_test, types.GeneratorType,
            "LocaleTemplateEnumerator generate_combinations did not return"
            " a generator object"
        )

        self.assertEqual(
            list(generator_test), test_values,
            "LocaleTemplateEnumerator generate_combinations did not generate "
            "all combinations"
        )

    def test_null_locale_argument(self):
        self.test_handler_input.request_envelope.request.locale = None
        generator_test = self.test_enumerator.generate_combinations(
            handler_input=self.test_handler_input,
            template_name=self.test_template_name)
        self.assertEqual(
            list(generator_test), [self.test_template_name],
            "LocaleTemplateEnumerator generate_combinations did not return "
            "template name as paths combinations when null locale is passed"
        )
