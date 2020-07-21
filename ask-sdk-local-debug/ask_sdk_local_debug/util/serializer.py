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
from ask_sdk_model_runtime import DefaultSerializer


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls

    def get_instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through get_instance()")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class Serializer(DefaultSerializer):
    def __init__(self):
        """Initialize the default serializer instance."""
        pass

    def __str__(self):
        return "Default Serializer object"
