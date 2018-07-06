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

from ask_sdk_model.services import ServiceClientFactory, ApiConfiguration
from ask_sdk_model import ResponseEnvelope

from .dispatch import RequestDispatcher
from .serialize import DefaultSerializer
from .handler_input import HandlerInput
from .exceptions import AskSdkException
from .attributes_manager import AttributesManager
from .utils import user_agent_info, RESPONSE_FORMAT_VERSION

if typing.TYPE_CHECKING:
    from typing import List, TypeVar, Any
    from ask_sdk_model.services import ApiClient
    from ask_sdk_model import RequestEnvelope
    from .dispatch_components import (
        RequestMapper, HandlerAdapter, ExceptionMapper,
        AbstractRequestInterceptor, AbstractResponseInterceptor)
    T = TypeVar['T']


class SkillConfiguration(object):
    """Configuration Object that represents standard components
    needed to build :py:class:`Skill`.

    :param request_mappers: List of request mapper instances.
    :type request_mappers: list(RequestMapper)
    :param handler_adapters: List of handler adapter instances.
    :type handler_adapters: list(HandlerAdapter)
    :param request_interceptors: List of
        request interceptor instances.
    :type request_interceptors: list(AbstractRequestInterceptor)
    :param response_interceptors: List of
        response interceptor instances.
    :type response_interceptors: list(AbstractResponseInterceptor)
    :param exception_mapper: Exception mapper instance.
    :type exception_mapper: ExceptionMapper
    :param persistence_adapter: Persistence adapter instance.
    :type persistence_adapter: AbstractPersistenceAdapter
    :param api_client: Api Client instance.
    :type api_client: ask_sdk_model.services.api_client.ApiClient
    :param custom_user_agent: Custom User Agent string
    :type custom_user_agent: str
    :param skill_id: ID of the skill.
    :type skill_id: str
    """

    def __init__(
            self, request_mappers, handler_adapters,
            request_interceptors=None, response_interceptors=None,
            exception_mapper=None, persistence_adapter=None,
            api_client=None, custom_user_agent=None, skill_id=None):
        # type: (List[RequestMapper], List[HandlerAdapter], List[AbstractRequestInterceptor], List[AbstractResponseInterceptor], ExceptionMapper, PersistenceAdapter, ApiClient, str, str) -> None
        """Configuration object that represents standard components
        needed for building :py:class:`Skill`.

        :param request_mappers: List of request mapper instances.
        :type request_mappers: list(RequestMapper)
        :param handler_adapters: List of handler adapter instances.
        :type handler_adapters: list(HandlerAdapter)
        :param request_interceptors: List of
            request interceptor instances.
        :type request_interceptors: list(AbstractRequestInterceptor)
        :param response_interceptors: List of
            response interceptor instances.
        :type response_interceptors: list(AbstractResponseInterceptor)
        :param exception_mapper: Exception mapper instance.
        :type exception_mapper: ExceptionMapper
        :param persistence_adapter: Persistence adapter instance.
        :type persistence_adapter: AbstractPersistenceAdapter
        :param api_client: Api Client instance.
        :type api_client: ask_sdk_model.services.api_client.ApiClient
        :param custom_user_agent: Custom User Agent string
        :type custom_user_agent: str
        :param skill_id: ID of the skill.
        :type skill_id: str
        """
        if request_mappers is None:
            request_mappers = []
        self.request_mappers = request_mappers

        if handler_adapters is None:
            handler_adapters = []
        self.handler_adapters = handler_adapters

        if request_interceptors is None:
            request_interceptors = []
        self.request_interceptors = request_interceptors

        if response_interceptors is None:
            response_interceptors = []
        self.response_interceptors = response_interceptors

        self.exception_mapper = exception_mapper
        self.persistence_adapter = persistence_adapter
        self.api_client = api_client
        self.custom_user_agent = custom_user_agent
        self.skill_id = skill_id


class Skill(object):
    """Top level container for Request Dispatcher,
    Persistence Adapter and Api Client.

    :param skill_configuration: Configuration object that holds
        information about different components needed to build the
        skill object.
    :type skill_configuration: SkillConfiguration
    """

    def __init__(self, skill_configuration):
        # type: (SkillConfiguration) -> None
        """Top level container for Request Dispatcher,
        Persistence Adapter and Api Client.

        :param skill_configuration: Configuration object that holds
            information about different components needed to build the
            skill object.
        :type skill_configuration: SkillConfiguration
        """
        self.persistence_adapter = skill_configuration.persistence_adapter
        self.api_client = skill_configuration.api_client
        self.serializer = DefaultSerializer()
        self.skill_id = skill_configuration.skill_id
        self.custom_user_agent = skill_configuration.custom_user_agent

        self.request_dispatcher = RequestDispatcher(
            request_mappers=skill_configuration.request_mappers,
            handler_adapters=skill_configuration.handler_adapters,
            exception_mapper=skill_configuration.exception_mapper,
            request_interceptors=skill_configuration.request_interceptors,
            response_interceptors=skill_configuration.response_interceptors)

    def invoke(self, request_envelope, context):
        # type: (RequestEnvelope, T) -> ResponseEnvelope
        """Invokes the dispatcher, to handle the request envelope and
        return a response envelope.

        :param request_envelope: Request Envelope instance containing
            request information
        :type request_envelope: RequestEnvelope
        :param context: Context passed during invocation
        :type context: Any
        :return: Response Envelope generated by handling the request
        :rtype: ResponseEnvelope
        """
        if (self.skill_id is not None and
                request_envelope.context.system.application.application_id !=
                self.skill_id):
            raise AskSdkException("Skill ID Verification failed!!")

        if self.api_client is not None:
            api_token = request_envelope.context.system.api_access_token
            api_endpoint = request_envelope.context.system.api_endpoint
            api_configuration = ApiConfiguration(
                serializer=self.serializer, api_client=self.api_client,
                authorization_value=api_token,
                api_endpoint=api_endpoint)
            factory = ServiceClientFactory(api_configuration=api_configuration)
        else:
            factory = None

        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=self.persistence_adapter)

        handler_input = HandlerInput(
            request_envelope=request_envelope,
            attributes_manager=attributes_manager,
            context=context,
            service_client_factory=factory)

        response = self.request_dispatcher.dispatch(handler_input)
        session_attributes = None

        if request_envelope.session is not None:
            session_attributes = (
                handler_input.attributes_manager.session_attributes)

        return ResponseEnvelope(
            response=response, version=RESPONSE_FORMAT_VERSION,
            session_attributes=session_attributes,
            user_agent=user_agent_info(self.custom_user_agent))
