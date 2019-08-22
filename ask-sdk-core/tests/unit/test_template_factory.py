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
import mock

from ask_sdk_core.view_resolvers.template_factory import TemplateFactory
from ask_sdk_core.view_resolvers.template_content import TemplateContent
from ask_sdk_runtime.view_resolvers.abstract_template_renderer import AbstractTemplateRenderer
from ask_sdk_runtime.view_resolvers.abstract_template_loader import AbstractTemplateLoader
from ask_sdk_core.exceptions import TemplateLoaderException, TemplateRendererException
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.response import Response


class TestTemplateFactory(unittest.TestCase):

    def setUp(self):
        self.test_loader = mock.MagicMock(spec=AbstractTemplateLoader)

        self.list_loaders = [self.test_loader]
        self.test_renderer = mock.MagicMock(spec=AbstractTemplateRenderer)
        self.test_template_content = mock.MagicMock(spec=TemplateContent)

        self.test_template_factory = TemplateFactory(
            template_loaders=self.list_loaders,
            template_renderer=self.test_renderer)
        self.test_template_name = 'test_template_name'
        self.test_data_map = {
            'test': 'test_data'
        }
        self.test_handler_input = mock.MagicMock(HandlerInput, autospec=True)

    def test_process_template_with_null_loaders(self):
        with self.assertRaises(ValueError) as exc:
            test_factory = TemplateFactory(template_loaders=None,
                                           template_renderer=self.test_renderer)
            test_factory.process_template(template_name=self.test_template_name,
                                          data_map=self.test_data_map,
                                          handler_input=self.test_handler_input)

        self.assertEqual(
            "Template Loaders list is null", str(exc.exception),
            "TemplateFactory did not raise ValueError for "
            "null list of loaders"

        )

    def test_process_template_with_null_renderer(self):
        with self.assertRaises(ValueError) as exc:
            test_factory = TemplateFactory(template_loaders=self.list_loaders,
                                           template_renderer=None)
            test_factory.process_template(template_name=self.test_template_name,
                                          data_map=self.test_data_map,
                                          handler_input=self.test_handler_input)
        self.assertEqual(
            "Template Renderer is null", str(exc.exception),
            "TemplateFactory did not raise ValueError for "
            "null renderer"

        )

    def test_process_template_for_null_template_name(self):
        with self.assertRaises(ValueError) as exc:
            self.test_template_factory.process_template(
                template_name=None, data_map=self.test_data_map,
                handler_input=self.test_handler_input)

        self.assertEqual(
            "Template Name is null", str(exc.exception),
            "TemplateFactory process_template did not raise ValueError for "
            "null template name"

        )

    def test_process_template_for_null_data_map(self):
        with self.assertRaises(ValueError) as exc:
            self.test_template_factory.process_template(
                template_name=self.test_template_name, data_map=None,
                handler_input=self.test_handler_input)

        self.assertEqual(
            "Data Map is null", str(exc.exception),
            "TemplateFactory process_template did not raise ValueError for "
            "null data map"

        )

    def test_process_template_with_no_matching_loader(self):
        with self.assertRaises(TemplateLoaderException) as exc:
            self.test_loader.load.return_value = None

            self.test_template_factory.process_template(
                template_name=self.test_template_name,
                data_map=self.test_data_map,
                handler_input=self.test_handler_input)

        self.assertEqual("Unable to load template: {} using provided loaders."
                         .format(self.test_template_name), str(exc.exception),
                         "TemplateFactory did not raise "
                         "TemplateResolverException if none of provided "
                         "loaders were unable to load the templates.")

    def test_process_template_raise_exception_at_load(self):
        with self.assertRaises(TemplateLoaderException) as exc:
            self.test_loader.load.side_effect = TemplateLoaderException(
                "Test Error")

            self.test_template_factory.process_template(
                template_name=self.test_template_name,
                data_map=self.test_data_map,
                handler_input=self.test_handler_input)

        self.assertEqual("Failed to load the template: {} using {} with error "
                         ": {}".format(self.test_template_name,
                                       self.test_loader, "Test Error"),
                         str(exc.exception), "TemplateFactory did not raise "
                                             "TemplateResolverException if none"
                                             " of provided loaders were unable"
                                             " to load the templates.")

    def test_process_template_raise_exception_at_render(self):
        with self.assertRaises(TemplateRendererException) as exc:
            self.test_loader.load.return_value = self.test_template_content
            self.test_renderer.render.side_effect = TemplateLoaderException(
                "Renderer Error")

            self.test_template_factory.process_template(
                template_name=self.test_template_name,
                data_map=self.test_data_map,
                handler_input=self.test_handler_input)

        self.assertEqual("Failed to render template: {} using {} with error: "
                         "{}".format(self.test_template_content, self.test_renderer,
                                     "Renderer Error"), str(exc.exception),
                         "TemplateFactory did not raise "
                         "TemplateResolverException if none of provided "
                         "loaders were unable to load the templates.")

    def test_process_template_returns_response(self):
        self.test_renderer.render.return_value = mock.MagicMock(
            Response, autospec=True)
        response = self.test_template_factory.process_template(
            template_name=self.test_template_name, data_map=self.test_data_map,
            handler_input=self.test_handler_input)
        self.assertIsInstance(response, Response,
                              "TemplateFactory process_template did not return"
                              "a Reponse object")