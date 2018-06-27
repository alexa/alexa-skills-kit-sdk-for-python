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


class ModelTestObject1(object):
    deserialized_types = {
        'str_var': 'str',
        'datetime_var': 'datetime',
        'obj_var': 'tests.unit.data.ModelTestObject2',
        'none_var': 'None',
        'enum_var': 'tests.unit.data.ModelEnumObject'
    }

    attribute_map = {
        'str_var': 'var1',
        'datetime_var': 'var2Time',
        'obj_var': 'var3Object',
        'none_var': 'var5None',
        'enum_var': 'var6Enum'
    }

    def __init__(self, str_var=None, datetime_var=None, obj_var=None, none_var=None, enum_var=None):
        self.str_var = str_var
        self.datetime_var = datetime_var
        self.obj_var = obj_var
        self.none_var = none_var
        self.enum_var = enum_var

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
