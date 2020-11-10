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
import typing
import importlib.util

from ask_sdk_local_debug.exception import LocalDebugSdkException

if typing.TYPE_CHECKING:
    from importlib._bootstrap import ModuleSpec
    from typing import Any


class SkillInvokerConfiguration(object):
    """Initialize skill invoker configuration class based on skill file path
    and skill handler arguments and sets up skill_invoker for local debug
    session.
    """

    def __init__(self, skill_file_path, skill_handler):
        # type: (str, str) -> None
        """Initialize skill invoker configuration class based on skill file
        path and skill handler arguments and sets up skill_invoker for local
        debug session.

        :param skill_file_path: The skills entry file for debug session.
        :type skill_file_path: str
        :param skill_handler: The skill handler to invoke for debug.
        :type skill_handler: str
        """
        self.skill_file_path = skill_file_path
        self.skill_handler = skill_handler
        self._spec = None  # type: ModuleSpec
        self.skill_builder_func = self.__get_skill_builder_func()

    @property
    def spec(self):
        # type: () -> Any
        """Returns the spec module loaded from the skill file path and skill
        handler.

        :return: Spec module from skill file path
        :rtype: object
        """
        try:
            self._spec = importlib.util.spec_from_file_location(
                self.skill_handler, self.skill_file_path)
        except Exception as e:
            raise LocalDebugSdkException(
                "Failed to import spec from the file location {} : {}".format(
                    self.skill_file_path, str(e)))
        return self._spec

    def __initialize_skill_invoker(self):
        # type: () -> Any
        """Returns a skill invoker module based on spec loaded from skill
        file path and skill handler.

        :return: Module used to invoke the skill handler.
        :rtype: object
        """
        try:
            skill_invoker = importlib.util.module_from_spec(self.spec)
            self.spec.loader.exec_module(skill_invoker)
        except Exception as e:
            raise LocalDebugSdkException(
                "Failed to load the module from {} : {}".format(
                    self.skill_file_path, str(e)))
        return skill_invoker

    def __get_skill_builder_func(self):
        try:
            return getattr(self.__initialize_skill_invoker(), self.skill_handler)
        except Exception as e:
            raise LocalDebugSdkException(
                "Handler function does not exist. Make sure that the skill file path:{} and "
                "the handler name:{} are correct. Exception:{}".format(
                    self.skill_file_path, self.skill_handler, str(e)))
