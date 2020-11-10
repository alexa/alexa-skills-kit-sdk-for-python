# -*- coding: utf-8 -*-
#
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights
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
from ask_sdk_local_debug.config.region import Region


class TestRegion(unittest.TestCase):
    def test_NA_endpoint(self):
        self.assertEqual('bob-dispatch-prod-na.amazon.com', Region['NA'].value)

    def test_EU_endpoint(self):
        self.assertEqual('bob-dispatch-prod-eu.amazon.com', Region['EU'].value)

    def test_FE_endpoint(self):
        self.assertEqual('bob-dispatch-prod-fe.amazon.com', Region['FE'].value)
