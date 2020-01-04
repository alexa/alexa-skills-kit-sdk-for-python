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
import typing
from ask_sdk_core.skill import CustomSkill
from ask_sdk_model import RequestEnvelope

from .verifier import RequestVerifier, TimestampVerifier

if typing.TYPE_CHECKING:
    from typing import Dict, Any, List
    from .verifier import AbstractVerifier


class WebserviceSkillHandler(object):
    """Skill Handler for skill as webservice.

    This class can be used by skill developers when they want their
    skills to be deployed as a web service, rather than using AWS
    Lambda.

    The class constructor takes in a custom skill instance that is
    used for routing the input request. The boolean verify_signature
    variable configures if the request signature is verified for each
    input request. The boolean verify_timestamp configures if the
    request timestamp is verified for each input request. Additionally,
    an optional list of verifiers can also be provided, to be applied
    on the input request.

    The `verify_request_and_dispatch` method provides the dispatch
    functionality that can be used as an entry point for skill
    invocation as web service.
    """
    def __init__(
            self, skill, verify_signature=True,
            verify_timestamp=True, verifiers=None):
        # type: (CustomSkill, bool, bool, List[AbstractVerifier]) -> None
        """Skill Handler for skill as webservice.

        This class can be used by skill developers when they want their
        skills to be deployed as a web service, rather than using AWS
        Lambda.

        The class constructor takes in a custom skill instance that is
        used for routing the input request. The boolean verify_signature
        variable configures if the request signature is verified for each
        input request. The boolean verify_timestamp configures if the
        request timestamp is verified for each input request. Additionally,
        an optional list of verifiers can also be provided, to be applied
        on the input request.

        :param skill: Custom skill instance containing registered
            request handlers and other components. If skill builders
            are being used to register the components, then the `create`
            method can be used to get this instance
        :type skill: ask_sdk_core.skill.CustomSkill
        :param verify_signature: Enable request signature verification
        :type verify_signature: bool
        :param verify_timestamp: Enable request timestamp verification
        :type verify_timestamp: bool
        :param verifiers: Optional list of verifiers that needs to be
            applied to the input request
        :type verifiers: list[
            ask_sdk_webservice_support.verifiers.AbstractVerifier]
        """
        self._skill = skill
        self._verifiers = []  # type: List[AbstractVerifier]

        if not isinstance(skill, CustomSkill):
            raise TypeError(
                "Invalid skill instance provided. Expected a custom "
                "skill instance.")

        self._add_custom_user_agent("ask-webservice")

        if verify_signature:
            self._verifiers.append(RequestVerifier())

        if verify_timestamp:
            self._verifiers.append(TimestampVerifier())

        if verifiers is not None:
            self._verifiers.extend(verifiers)

    def _add_custom_user_agent(self, user_agent):
        # type: (str) -> None
        """Adds the user agent to the skill instance.

        This method adds the passed in user_agent to the skill, which
        is reflected in the skill's response envelope.

        :param user_agent: Custom User Agent string provided by
            the developer.
        :type user_agent: str
        :rtype: None
        """
        if self._skill.custom_user_agent is None:
            self._skill.custom_user_agent = user_agent
        else:
            self._skill.custom_user_agent += " {}".format(user_agent)

    def verify_request_and_dispatch(
            self, http_request_headers, http_request_body):
        # type: (Dict[str, Any], str) -> str
        """Entry point for webservice skill invocation.

        This method takes in the input request headers and request body,
        handles the deserialization of the input request to
        the :py:class:`ask_sdk_model.request_envelope.RequestEnvelope`
        object, run the input through registered verifiers, invoke the
        skill and return the serialized response from the
        skill invocation.

        :param http_request_headers: Request headers of the input
            request to the webservice
        :type http_request_headers: Dict[str, Any]
        :param http_request_body: Raw request body of the input request
            to the webservice
        :type http_request_body: str
        :return: Serialized response object returned by the skill
            instance, when invoked with the input request
        :rtype: str
        :raises: :py:class:`ask_sdk_core.exceptions.AskSdkException`
            when skill deserialization, verification, invocation or
            serialization fails
        """
        request_envelope = self._skill.serializer.deserialize(
            payload=http_request_body, obj_type=RequestEnvelope)

        for verifier in self._verifiers:
            verifier.verify(
                headers=http_request_headers,
                serialized_request_env=http_request_body,
                deserialized_request_env=request_envelope)

        response_envelope = self._skill.invoke(
            request_envelope=request_envelope, context=None)

        return self._skill.serializer.serialize(response_envelope)  # type: ignore
