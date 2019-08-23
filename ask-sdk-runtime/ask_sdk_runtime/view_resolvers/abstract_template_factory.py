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
import typing

from abc import ABCMeta, abstractmethod

if typing.TYPE_CHECKING:
    from typing import Dict
    from ask_sdk_model import Response


class AbstractTemplateFactory(object):
    """Template Factory interface to process template and data to generate
    skill response.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_template(self, template_name, data_map):
        # type: (str, Dict) -> Response
        """Process response template and data to generate skill response.

        :param template_name: Template name
        :type template_name: str
        :param data_map: Map of template content slot values
        :type data_map: Dict[str, object]
        :return: Skill Response output
        :rtype: :py:class:`ask_sdk_model.response.Response`
        """
        pass
