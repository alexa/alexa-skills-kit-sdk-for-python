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
try:
    import mock
except ImportError:
    from unittest import mock

from mock import patch
from io import StringIO
from ask_sdk_model import RequestEnvelope
from ask_sdk_model.canfulfill import CanFulfillIntentRequest
from ask_sdk_runtime.view_resolvers import (
    AbstractTemplateEnumerator, AbstractTemplateCache
)
from ask_sdk_core.view_resolvers import (
    FileSystemTemplateLoader, LocaleTemplateEnumerator, LRUCache)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.exceptions import TemplateLoaderException



class TestCustomEnumerator(AbstractTemplateEnumerator):
    def generate_combinations(self, handler_input, template_name):
        return ['test']


class TestFileSystemTemplateLoader(unittest.TestCase):
    @patch('ask_sdk_core.view_resolvers.locale_template_enumerator'
           '.LocaleTemplateEnumerator', autospec=True)
    @patch('ask_sdk_core.view_resolvers.lru_cache.LRUCache', autospec=True)
    def setUp(self, mock_cache, mock_enumerator):
        self.test_template_name = 'test'
        self.test_dir_path = '.'
        self.test_enumerator = mock_enumerator.return_value
        mock_cache.get.return_value = None
        self.cache = mock_cache
        self.test_handler_input = HandlerInput(request_envelope=RequestEnvelope(
            request=CanFulfillIntentRequest(locale='en-GB')))
        self.test_loader = FileSystemTemplateLoader(dir_path=self.test_dir_path,
                                                    enumerator=self.test_enumerator,
                                                    cache=mock_cache,
                                                    encoding='utf-8')

    def test_loader_with_null_dir_path(self):
        with self.assertRaises(ValueError) as exc:
            FileSystemTemplateLoader(dir_path=None, enumerator=None)

        self.assertEqual(
            "Directory path is null", str(exc.exception),
            "LocaleTemplateLoader did not raise ValueError on"
            "null directory path"
        )

    def test_loader_with_null_template_name(self):
        with self.assertRaises(ValueError) as exc:
            self.test_loader.load(handler_input=self.test_handler_input,
                                  template_name=None)

        self.assertEqual(
            "Template Name is null", str(exc.exception),
            "LocaleTemplateLoader did not raise ValueError on"
            "null template name"
        )

    def test_load_returns_none_for_invalid_file_paths_during_enumeration(self):
        self.test_enumerator.generate_combinations.return_value = ['test']
        loader = self.test_loader.load(handler_input=self.test_handler_input,
                                       template_name=self.test_template_name)
        self.assertEqual(
            loader, None,
            "LocaleTemplateLoader load method did not return None for invalid"
            "file paths from generate_combinations"
        )

    @patch('ask_sdk_core.view_resolvers.file_system_template_loader.os')
    @patch('ask_sdk_core.view_resolvers.file_system_template_loader.io')
    def test_loading_template_data_to_template_view(self, mock_open, mock_os):
        test_response_template = u'test data'
        self.test_enumerator.generate_combinations.return_value = ['response']
        mock_os.path.exists.return_value = True
        mock_open.open.return_value.__enter__.return_value = StringIO(
                                                        test_response_template)
        loader = self.test_loader.load(handler_input=self.test_handler_input,
                                       template_name=self.test_template_name)
        self.assertEqual(
            loader.content_data.decode('utf-8'), test_response_template,
            "FileSystemLoader loader did not load proper template data into "
            "TemplateView object"
        )

    @patch('ask_sdk_core.view_resolvers.file_system_template_loader.os')
    @patch('ask_sdk_core.view_resolvers.file_system_template_loader.io')
    def test_loading_template_data_from_cache(self, mock_open, mock_os):
        test_response_template = u'test data'
        test_path_value = './test'
        self.test_enumerator.generate_combinations.return_value = ['response']
        mock_os.path.exists.return_value = True
        mock_os.path.join.return_value = test_path_value
        mock_open.open.return_value.__enter__.return_value = StringIO(
                                                        test_response_template)
        template_content = self.test_loader.load(
            handler_input=self.test_handler_input,
            template_name=self.test_template_name)

        self.assertTrue(
            self.cache.put.called, "FileSystemLoader did not load the "
                                   "template content into cache"
        )

        self.assertEqual(
            template_content.content_data.decode('utf-8'), test_response_template,
            "FileSystemLoader loader did not load proper template data into "
            "TemplateView object"
        )

        self.cache.get.return_value = template_content

        _ = self.test_loader.load(
            handler_input=self.test_handler_input,
            template_name=self.test_template_name)

        self.assertEqual(
            self.cache.put.call_count, 1,
            "FileSystemLoader did not try to load template from cache"
        )

        self.assertEqual(
            self.cache.get.call_count, 2,
            "FileSystemLoader did not try to load template from cache"
        )

    def test_exceptions_raised_in_load(self):
        self.test_enumerator.generate_combinations.side_effect = (
            TemplateLoaderException("test enumeration exception"))
        with self.assertRaises(TemplateLoaderException) as exc:
            _loader = self.test_loader.load(
                handler_input=self.test_handler_input,
                template_name=self.test_template_name)

        self.assertEqual(
            "Failed to load the template : test "
            "error : test enumeration exception", str(exc.exception),
            "FileSystemLoader did not raise TemplateResolverException"
            "when enumeration throws error"
        )

    def test_validate_enumerator_for_null_enumerator(self):
        test_enumerator = FileSystemTemplateLoader.validate_enumerator(
            enumerator=None)
        self.assertIsInstance(
            test_enumerator, LocaleTemplateEnumerator,
            "validate_enumerator did not create default "
            "LocaleTemplateEnumerator when null was passed as enumerator"
        )

    def test_validate_enumerator_for_instance_type(self):
        with self.assertRaises(TypeError) as exc:
            FileSystemTemplateLoader.validate_enumerator(
                enumerator='test')

        self.assertEqual("The provided enumerator is not of type "
                         "AbstractTemplateEnumerator", str(exc.exception),
                         "validate_enumerator did not raise TypeError for "
                         "invalid enumerator instance")

    @patch('ask_sdk_core.view_resolvers.file_system_template_loader.os')
    @patch('ask_sdk_core.view_resolvers.file_system_template_loader.'
           'append_extension_if_not_exists')
    def test_custom_enumerator_for_loader(self, mock_function, mock_os):
        custom_enumerator = TestCustomEnumerator()
        mock_os.path.exists.return_value = False
        custom_loader = FileSystemTemplateLoader(dir_path=self.test_dir_path,
                                                 enumerator=custom_enumerator)
        custom_loader.load(handler_input=self.test_handler_input,
                           template_name=self.test_template_name)
        args, kwargs = mock_function.call_args
        self.assertEqual(args, ('test', None), "FileSystemTemplateLoader "
                                               "failed to use custom "
                                               "enumerator to generate path "
                                               "combinations")

    def test_validate_cache_for_null(self):
        test_cache = FileSystemTemplateLoader.validate_cache(
            cache=None)
        self.assertIsInstance(
            test_cache, LRUCache,
            "validate_cache did not create default LRUCache"
            " when null was passed as cache"
        )

    def test_validate_cache_for_instance_type(self):
        with self.assertRaises(TypeError) as exc:
            FileSystemTemplateLoader.validate_cache(
                cache='test')

        self.assertEqual("The provided cache is not of type "
                         "AbstractTemplateCache", str(exc.exception),
                         "validate_enumerator did not raise TypeError for "
                         "invalid cache instance")

    def test_custom_cache_for_loader(self):
        custom_cache = mock.MagicMock(spec=AbstractTemplateCache)
        custom_loader = FileSystemTemplateLoader(dir_path=self.test_dir_path,
                                                 cache=custom_cache)

        self.assertIsInstance(
            custom_loader.template_cache, AbstractTemplateCache,
            "The provided cache instance is not of type AbstractTemplateCache"
        )
