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

from ask_sdk_core.utils.view_resolver import (
    split_locale, append_extension_if_not_exists, assert_not_null)


class TestViewResolverUtils(unittest.TestCase):

    def test_split_locale_return_values(self):
        test_locale = 'en-GB'
        language, country = split_locale(locale=test_locale)
        self.assertEqual(
            language, 'en', "split_locale could not return language "
                            "from locale"
        )

        self.assertEqual(
            country, 'GB', "split_locale could not return country from locale"
        )

    def test_split_locale_for_null_locale(self):
        language, country = split_locale(locale=None)
        self.assertEqual(
            (language, country), (None, None), "split_locale could not return "
                                               "language from locale"
        )

    def test_split_locale_raises_error_for_invalid_locale(self):
        test_locale = 'en-GBAA'
        with self.assertRaises(ValueError) as exc:
            split_locale(locale=test_locale)

        self.assertIn("Invalid locale: {}".format(test_locale),
                      str(exc.exception), "split_locale did not raise "
                                          "ValueError for invalid locale")

    def test_append_extension_if_not_exists(self):
        test_file_path = 'response'
        test_file_extension = 'jinja'
        result = append_extension_if_not_exists(
            file_path=test_file_path, file_extension=test_file_extension)
        self.assertEqual(
            result, 'response.jinja', "append_extension_if_not_exists did not "
                                      "appended extension to file path"
        )

    def test_append_extension_if_not_exists_with_duplicate_file_extension(self):
        test_file_path = 'response.jinja'
        test_file_extension = 'jinja'
        result = append_extension_if_not_exists(
            file_path=test_file_path, file_extension=test_file_extension)
        self.assertEqual(
            result, test_file_path, "append_extension_if_not_exists appended "
                                    "extension to file path which had "
                                    "extension defined already"
        )

    def test_assert_not_null(self):
        test_obj = None
        with self.assertRaises(ValueError) as exc:
            assert_not_null(attribute=test_obj, value='Test object')

        self.assertIn(
            "{} is null".format('Test object'), str(exc.exception),
            "assert_not_null did not raise ValueError for null attributes"
        )

    def test_assert_not_null_with_empty_attribute(self):
        test_object = 'test'
        test_result = assert_not_null(attribute=test_object,
                                      value='test value')

        self.assertEqual(test_result, test_object, "assert_not_null did not "
                                                   "return the same attribute")
