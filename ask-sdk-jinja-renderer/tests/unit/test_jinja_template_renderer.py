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

from ask_sdk_jinja_renderer.jinja_template_renderer import JinjaTemplateRenderer
from ask_sdk_core.exceptions import TemplateRendererException
from ask_sdk_core.view_resolvers.template_content import TemplateContent
from ask_sdk_model import Response
from jinja2 import Template


class TestJinjaTemplateRenderer(unittest.TestCase):

    def setUp(self):
        self.jinja_renderer = JinjaTemplateRenderer()
        self.template_content = mock.MagicMock(spec=TemplateContent)
        self.template = mock.MagicMock(spec=Template)
        self.test_data_map = {
            'test': 'test_data'
        }

    def test_render_raise_exception(self):
        with self.assertRaises(TemplateRendererException) as exc:
            mock_property = mock.PropertyMock(
                side_effect=TemplateRendererException("Renderer Error"))
            type(self.template_content).encoding = mock_property
            self.jinja_renderer.render(template_content=self.template_content,
                                       data_map=self.test_data_map)

        self.assertEqual("Failed to render the template error : Renderer Error",
                         str(exc.exception),
                         "JinjaTemplateRenderer failed to raise "
                         "TemplateResolverException")

    @mock.patch('ask_sdk_jinja_renderer.jinja_template_renderer.DefaultSerializer')
    def test_render_return_response(self, mock_serializer):
        test_template = b'{"test": "test_data"}'
        mock_property = mock.PropertyMock(return_value='utf-8')
        mock_property_content = mock.PropertyMock(return_value=test_template)
        type(self.template_content).encoding = mock_property
        type(self.template_content).content_data = mock_property_content
        mock_serializer.return_value.deserialize.return_value = mock.MagicMock(
            spec=Response)
        test_jinja_renderer = JinjaTemplateRenderer()
        response = test_jinja_renderer.render(
            template_content=self.template_content, data_map=self.test_data_map)

        self.assertIsInstance(response, Response, "JinjaTemplateRenderer "
                                                  "render did not return "
                                                  "Response object")
