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
from abc import ABCMeta, abstractmethod


class ModelAbstractParentObject(object):
    __metaclass__ = ABCMeta

    deserialized_types = {
        'child_type': 'str',
        'str_var': 'str',
        'obj_var': 'tests.unit.data.ModelTestObject2',
    }

    attribute_map = {
        'child_type': 'ChildType',
        'str_var': 'var1',
        'obj_var': 'var3Object',
    }

    discriminator_value_class_map = {
        'ChildType1': 'tests.unit.data.ModelChildObject1',
        'ChildType2': 'tests.unit.data.ModelChildObject2'
    }

    json_discriminator_key = "ChildType"

    @abstractmethod
    def __init__(self, child_type=None, str_var=None, obj_var=None):
        self.child_type = child_type
        self.str_var = str_var
        self.obj_var = obj_var

    @classmethod
    def get_real_child_model(cls, data):
        """Returns the real base class specified by the discriminator"""
        discriminator_value = data[cls.json_discriminator_key]
        return cls.discriminator_value_class_map.get(discriminator_value)