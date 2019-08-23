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

import typing
from abc import ABCMeta, abstractmethod

if typing.TYPE_CHECKING:
    from typing import Any, Optional
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.view_resolvers import TemplateContent


class AbstractTemplateLoader(object):
    """Given template name, load template from data source and store
    it as string on TemplateContent object.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, handler_input, template_name, **kwargs):
        # type: (HandlerInput, str, Any) -> Optional[TemplateContent]
        """Loads the given input template data into a TemplateContent object.

        :param handler_input: Handler Input instance with
            Request Envelope containing Request.
        :type  handler_input: :py:class:`ask_sdk_core.handler_input.HandlerInput`
        :param template_name: Template name to be loaded
        :type template_name: str
        :return: (optional) TemplateContent
        :rtype: :py:class:`ask_sdk_core.view_resolvers.TemplateContent`
        """
        pass
