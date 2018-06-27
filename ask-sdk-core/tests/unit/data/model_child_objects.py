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
import six

from .model_abstract_parent_object import ModelAbstractParentObject


class ModelChildObject1(ModelAbstractParentObject):
    deserialized_types = {
        'child_type': 'str',
        'str_var': 'str',
        'obj_var': 'tests.unit.data.ModelTestObject2',
        'test_var': 'str'
    }

    attribute_map = {
        'child_type': 'ChildType',
        'str_var': 'var1',
        'obj_var': 'var3Object',
        'test_var': 'testVar'
    }

    def __init__(self, str_var=None, obj_var=None, test_var=None):
        super(ModelChildObject1, self).__init__(child_type="ChildType1", str_var=str_var, obj_var=obj_var)
        self.test_var = test_var

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ModelChildObject2(ModelAbstractParentObject):
    deserialized_types = {
        'child_type': 'str',
        'str_var': 'str',
        'obj_var': 'tests.unit.data.ModelTestObject2',
        'test_int_var': 'int'
    }

    attribute_map = {
        'child_type': 'ChildType',
        'str_var': 'var1',
        'obj_var': 'var3Object',
        'test_int_var': 'testIntVar'
    }

    def __init__(self, str_var=None, obj_var=None, test_int_var=None):
        super(ModelChildObject2, self).__init__(child_type="ChildType2", str_var=str_var, obj_var=obj_var)
        self.test_int_var = test_int_var

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
