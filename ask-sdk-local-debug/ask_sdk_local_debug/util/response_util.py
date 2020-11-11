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
import logging
import typing
import json
from http import HTTPStatus

from ask_sdk_model.dynamic_endpoints import (FailureResponse, Request,
                                             SuccessResponse)
from ask_sdk_local_debug.util.serializer import Serializer
from ask_sdk_local_debug.exception import LocalDebugSdkException

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from ask_sdk_local_debug.config.skill_invoker_config import SkillInvokerConfiguration
    from ask_sdk_model.dynamic_endpoints.base_response import BaseResponse


def get_local_debug_failure_response(local_debug_request, exception):
    # type: (Request, Exception) -> FailureResponse
    """Builds a failure response for runtime exception encountered when
    invoking skill code.

    :param local_debug_request: Skill request parameter.
    :type local_debug_request: :py:class:`ask_sdk_model.dynamic_endpoints.Request`
    :param exception: Exception object available when skill invocation results
        in an error.
    :type exception: Exception class object.
    :return: Skill failure response.
    :rtype: :py:class:`ask_sdk_model.dynamic_endpoints.FailureResponse`
    """
    try:
        return FailureResponse(version=local_debug_request.version,
                               original_request_id=local_debug_request.request_id,
                               error_code=str(
                                   HTTPStatus.INTERNAL_SERVER_ERROR.value),
                               error_message=str(exception))
    except Exception as ex:
        logger.error(
            "Failed to create FailureResponse instance : {}".format(str(ex)))
        raise LocalDebugSdkException("Failed to create FailureResponse "
                                     "instance : {}".format(str(ex)))


def get_local_debug_success_response(local_debug_request,
                                     skill_success_response):
    # type: (Request, str) -> SuccessResponse
    """Builds a success response for response payload obtained when
    invoking skill code.

    :param local_debug_request: Skill request parameter.
    :type local_debug_request: :py:class:`ask_sdk_model.dynamic_endpoints.Request`
    :param skill_success_response: Skill Response.
    :type skill_success_response: str
    :return: Skill success response.
    :rtype: :py:class:`ask_sdk_model.dynamic_endpoints.SuccessResponse`
    """
    try:
        return SuccessResponse(
            original_request_id=local_debug_request.request_id,
            response_payload=skill_success_response,
            version=local_debug_request.version)
    except Exception as ex:
        logger.error(
            "Failed to create SuccessResponse instance : {}".format(str(ex)))
        raise LocalDebugSdkException("Failed to create SuccessResponse "
                                     "instance : {}".format(str(ex)))


def get_skill_response(local_debug_request, skill_invoker_config):
    # type: (Request, SkillInvokerConfiguration) -> str
    """Invokes skill code with skill request payload.

    :param local_debug_request: Skill request payload.
    :type local_debug_request: :py:class:`ask_sdk_model.dynamic_endpoints.Request`
    :param skill_invoker_config: Skill Invoker instance to invoke skill code
    :type skill_invoker_config: :py:class:`ask_sdk_local_debug.skill_invoker_config.SkillInvokerConfiguration`
    :return: Response payload.
    :rtype: str
    """
    try:
        request_envelope = json.loads(local_debug_request.request_payload)
        default_serializer = Serializer.get_instance()  # type: ignore
        response_payload = None  # type: BaseResponse

        try:
            skill_response = skill_invoker_config.skill_builder_func(request_envelope, None)
        except Exception as ex:
            logger.error(
                "Failed to retrieve skill response : {}".format(str(ex)))
            response_payload = get_local_debug_failure_response(
                local_debug_request=local_debug_request, exception=ex)

        if response_payload is None:
            skill_response = json.dumps(skill_response)
            response_payload = get_local_debug_success_response(
                local_debug_request=local_debug_request,
                skill_success_response=skill_response)
        serialized_response = default_serializer.serialize(response_payload)

        return json.dumps(serialized_response)
    except Exception as ex:
        logger.error("Error in get_skill_response : {}".format(str(ex)))
        raise LocalDebugSdkException(
            "Error in get_skill_response : {}".format(str(ex)))


def get_deserialized_request(skill_request_payload):
    # type:(str) -> Request
    """Deserialize the incoming request payload into
    :py:class:`ask_sdk_model.dynamic_endpoints.Request` class.

    :param skill_request_payload: Incoming skill request payload.
    :type skill_request_payload: str
    :return: Serialized skill request.
    :rtype: :py:class:`ask_sdk_model.dynamic_endpoints.Request
    """
    try:
        default_serializer = Serializer.get_instance()  # type: ignore
        return default_serializer.deserialize(payload=skill_request_payload,
                                              obj_type=Request)
    except Exception as ex:
        logger.error("Failed to deserialize request : {}".format(str(ex)))
        raise LocalDebugSdkException(
            "Failed to deserialize skill_request : {}".format(str(ex)))
