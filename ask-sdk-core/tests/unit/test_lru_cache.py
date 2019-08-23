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

from ask_sdk_core.view_resolvers.lru_cache import LRUCache
from ask_sdk_core.view_resolvers.template_content import TemplateContent


class TestLRUCache(unittest.TestCase):

    def setUp(self):
        self.test_cache = LRUCache(capacity=10, time_to_live=1000)
        self.template_content = TemplateContent(content_data=b'test',
                                                encoding='utf-8')
        self.template_content_2 = TemplateContent(
            content_data=b'test data out of capacity string length',
            encoding='utf-8')

    def test_put_within_capacity(self):
        self.test_cache.put(key='/', template_content=self.template_content)
        self.assertEqual(
            self.test_cache._current_capacity, 4,
            "LRUCache didn't cache the template content")

    def test_put_out_of_capacity(self):
        self.test_cache.put(key='/', template_content=self.template_content_2)

        self.assertEqual(
            self.test_cache._current_capacity, 0,
            "LRUCache cached the template which is out of its capacity"
        )

    def test_put_cache_eviction(self):
        self.test_cache.put(key='/', template_content=self.template_content)
        self.test_cache.put(key='/', template_content=self.template_content)
        self.test_cache.put(key='/test', template_content=self.template_content)
        self.test_cache.put(key='/local/test',
                            template_content=self.template_content)

        self.assertEqual(
            self.test_cache._current_capacity, 8,
            "LRUCache did not evict the LRU used data from it's cache"
        )

        self.assertEqual(
            len(self.test_cache._template_data_map), 2,
            "LRUCache did not evict the LRU used data from it's cache"
        )

    def test_cache_get_template(self):
        test_key = '/test'
        self.test_cache.put(key=test_key,
                            template_content=self.template_content)

        template = self.test_cache.get(key=test_key)
        self.assertEqual(
            template.content_data, self.template_content.content_data,
            "LRU Cache could not retrieve template data from cache"
        )

    def test_cache_get_stale_template_returns_null(self):
        test_key = '/test'
        test_cache = LRUCache(time_to_live=0)
        test_cache.put(key=test_key, template_content=self.template_content)
        template = test_cache.get(key=test_key)
        self.assertIsNone(
            template, "LRU Cache could retrieve stale template data from cache"
        )
