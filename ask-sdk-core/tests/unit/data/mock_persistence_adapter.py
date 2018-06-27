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
from ask_sdk_core.attributes_manager import AbstractPersistenceAdapter


class MockPersistenceAdapter(AbstractPersistenceAdapter):
    def __init__(self):
        self.attributes = {"key_1": "v1", "key_2": "v2"}
        self.get_count = 0
        self.save_count = 0

    def get_attributes(self, request_envelope):
        self.get_count += 1
        return self.attributes

    def save_attributes(self, request_envelope, attributes):
        self.save_count += 1
        self.attributes = attributes

