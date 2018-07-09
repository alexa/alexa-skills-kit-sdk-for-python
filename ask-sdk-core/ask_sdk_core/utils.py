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
import sys
import typing

from ask_sdk_model import IntentRequest

from .__version__ import __version__

if typing.TYPE_CHECKING:
    from typing import Callable
    from .handler_input import HandlerInput


SDK_VERSION = __version__
RESPONSE_FORMAT_VERSION = "1.0"


def user_agent_info(custom_user_agent):
    # type: (str) -> str
    """Return the user agent info along with the SDK and Python
    Version information.

    :param custom_user_agent: Custom User Agent string provided by
        the developer.
    :type custom_user_agent: str
    :return: User Agent Info string
    :rtype: str
    """
    python_version = ".".join(str(x) for x in sys.version_info[0:3])
    user_agent = "ask-python/{} Python/{}".format(
        SDK_VERSION, python_version)
    if custom_user_agent is None:
        return user_agent
    else:
        return user_agent + " {}".format(custom_user_agent)


def is_intent_name(name):
    # type: (str) -> Callable[[HandlerInput], bool]
    """A predicate function returning a boolean, when name matches the
    name in Intent Request.

    The function can be applied on a
    :py:class:`ask_sdk_core.handler_input.HandlerInput`, to
    check if the input is of
    :py:class:`ask_sdk_model.intent_request.IntentRequest` type and if the
    name of the request matches with the passed name.

    :param name: Name to be matched with the Intent Request Name
    :type name: str
    :return: Predicate function that can be used to check name of the
        request
    :rtype: Callable[[HandlerInput], bool]
    """
    def can_handle_wrapper(handler_input):
        # type: (HandlerInput) -> bool
        return (isinstance(
            handler_input.request_envelope.request, IntentRequest) and
                handler_input.request_envelope.request.intent.name == name)
    return can_handle_wrapper


def is_request_type(request_type):
    # type: (str) -> Callable[[HandlerInput], bool]
    """A predicate function returning a boolean, when request type is
    the passed-in type.

    The function can be applied on a
    :py:class:`ask_sdk_core.handler_input.HandlerInput`, to check
    if the input request type is the passed in request type.

    :param request_type: request type to be matched with the input's request
    :type request_type: str
    :return: Predicate function that can be used to check the type of
        the request
    :rtype: Callable[[HandlerInput], bool]
    """
    def can_handle_wrapper(handler_input):
        # type: (HandlerInput) -> bool
        return (handler_input.request_envelope.request.object_type ==
                request_type)
    return can_handle_wrapper
