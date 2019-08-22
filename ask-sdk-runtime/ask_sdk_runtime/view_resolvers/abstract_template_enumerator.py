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
    from typing import Iterator
    from ask_sdk_core.handler_input import HandlerInput


class AbstractTemplateEnumerator(object):
    """Enumerator to enumerate template name based on specific property."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_combinations(self, handler_input, template_name):
        # type: (HandlerInput, str) -> Iterator[str]
        """Generate string combinations of template name and other properties.

        This method has to be implemented, to enumerate on different
        combinations of template name and other properties in handler input
        (eg: locale, attributes etc.), that is checked during loading the
        template.

        :param handler_input: Handler Input instance with
            Request Envelope containing Request.
        :type  handler_input: :py:class:`ask_sdk_core.handler_input.HandlerInput`
        :param template_name: Template name which needs to be loaded
        :type template_name: str
        :return: Generator object which returns relative paths of the template
        :rtype: Iterator[str]
        """
        pass
