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
import six

from ask_sdk_runtime.view_resolvers import AbstractTemplateRenderer
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.exceptions import TemplateRendererException
from jinja2 import Template

if typing.TYPE_CHECKING:
    from typing import TypeVar, Dict, Any, Union
    from ask_sdk_core.view_resolvers.template_content import TemplateContent
    from ask_sdk_model.services import Serializer
    T = TypeVar('T')


class JinjaTemplateRenderer(AbstractTemplateRenderer):
    """Implementation to render a Jinja Template, and deserialize to skill
    response output.

    JinjaTemplateRenderer can be initialised with a custom serializer to
    deserialize the template content to corresponding response type.

    If no serializer is specified, default serializer from
    :py:class:`ask_sdk_core.serialize.DefaultSerializer` is set also if the
    output type is not specified default value of
    :py:class:`ask_sdk_model.response.Response` is set.

    The ``output_type`` parameter can be a primitive type, a generic
    model object or a list / dict of model objects.

    :param serializer: Serializer to deserialize template content
    :type serializer: :py:class:`ask_sdk_model.services.Serializer`
    :param output_type: resolved class name for deserialized object
    :type output_type: Union[object, str]
    """
    def __init__(self, serializer=None, output_type=None):
        # type: (Serializer, Union[T, str]) -> None
        """Initializing the default serializer to deserialize rendered content
        to skill response output.

        If no serializer is specified, default serializer from
        :py:class:`ask_sdk_core.serialize.DefaultSerializer` is set also if the
        output type is not specified default value of
        :py:class:`ask_sdk_model.response.Response` is set.

        The ``output_type`` parameter can be a primitive type, a generic
        model object or a list / dict of model objects.

        :param serializer: Serializer to deserialize template content
        :type serializer: :py:class:`ask_sdk_model.services.Serializer`
        :param output_type: resolved class name for deserialized object
        :type output_type: Union[object, str]
        """
        self.serializer = serializer
        self.output_type = output_type

        if self.serializer is None:
            self.serializer = DefaultSerializer()
        if self.output_type is None:
            self.output_type = 'ask_sdk_model.response.Response'

    def render(self, template_content, data_map, **kwargs):
        # type: (TemplateContent, Dict, Any) -> Any
        """Render :py:class:`ask_sdk_core.view_resolvers.TemplateContent` by
        processing data and deserialize to skill response output.

        :param template_content: TemplateContent that contains template data
        :type template_content: :py:class:`ask_sdk_core.view_resolvers.TemplateContent`
        :param data_map: Map that contains injecting data values to template
        :type data_map: Dict[str, object]
        :param **kwargs: Optional arguments that renderer takes.
        :return: Skill Response output, defaults to :py:class:`ask_sdk_model.Response`
        :rtype: Any
        :raises: :py:class:`ask_sdk_core.exceptions.TemplateResolverException`
            if rendering of the template fails.
        """
        try:
            encoding = template_content.encoding
            template = Template(template_content.content_data.decode(encoding))
            rendered_template = template.render(data_map)
            if six.PY2:
                rendered_template = rendered_template.encode("utf-8")
            return self.serializer.deserialize(rendered_template, self.output_type)
        except Exception as e:
            raise TemplateRendererException("Failed to render the template "
                                            "error : {}".format(str(e)))
