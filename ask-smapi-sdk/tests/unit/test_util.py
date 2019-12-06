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
from ask_smapi_sdk import get_header_value


class TestUtils(unittest.TestCase):
    def test_get_header_value_null_header_list(self):
        result = get_header_value(header_list=None, key='test_key')
        self.assertEqual(result, [],("get_header_value did not return empty "
                                     "list for empty header_list"))
                            
    def test_get_header_value_multiple_keys(self):
        mock_header_list = [('Content-Type', 'application/json'),
                            ('Content-Length', '98'),
                            ('Connection', 'keep-alive'),
                            ('Server', 'Test Server 1'),
                            ('Server', 'Test Server 2'),
                            ('Server', 'Test Server 3')]
        test_key = 'Server'
        test_result = ['Test Server 1', 'Test Server 2', 'Test Server 3']
        result = get_header_value(header_list=mock_header_list, key=test_key)

        self.assertEqual(result, test_result, ("get_header_value did not "
                                               "return the list of values for "
                                               "{}".format(test_key)))

    def test_get_header_value_invalid_key(self):
        mock_header_list = [('Content-Type', 'application/json'),
                            ('Content-Length', '98'), ('Connection', 'keep-alive'),
                            ('Server', 'Test Server')]
        test_key = 'Location'
        result = get_header_value(header_list=mock_header_list, key=test_key)
        self.assertEqual(result, [], ("get_header_value did not return empty "
                                      "list for {}".format(test_key)))