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


class ModelTestObject2(object):
    deserialized_types = {
        'int_var': 'int'
    }

    attribute_map = {
        'int_var': 'var4Int'
    }

    def __init__(self, int_var=None):
        self.int_var = int_var

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
