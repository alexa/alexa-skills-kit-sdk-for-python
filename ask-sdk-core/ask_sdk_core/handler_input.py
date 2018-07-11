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
from .response_helper import ResponseFactory

if typing.TYPE_CHECKING:
    from ask_sdk_model import Context, RequestEnvelope
    from ask_sdk_model.services import ServiceClientFactory
    from .attributes_manager import AttributesManager


class HandlerInput(object):
    """Input to Request Handler, Exception Handler and Interceptors.

    Handler Input instantiations are passed to the registered instances
    of `AbstractRequestHandler` and `AbstractExceptionHandler`
    , during skill invocation. The class provides a `AttributesManager`
    and a `ResponseFactory` instance, apart from `RequestEnvelope`,
    `Context` and `ServiceClientFactory` instances, to utilize during
    the lifecycle of skill.

    :param request_envelope: Request Envelope passed from Alexa
            Service
    :type request_envelope: ask_sdk_model.request_envelope.RequestEnvelope
    :param attributes_manager: Attribute Manager instance for
        managing attributes across skill lifecycle
    :type attributes_manager:
        ask_sdk_core.attributes_manager.AttributesManager
    :param context: Context object passed from Lambda service
    :type context: object
    :param service_client_factory: Service Client Factory instance
        for calling Alexa services
    :type service_client_factory:
        ask_sdk_model.services.service_client_factory.ServiceClientFactory
    """
    def __init__(
            self, request_envelope, attributes_manager=None,
            context=None, service_client_factory=None):
        # type: (RequestEnvelope, AttributesManager, Context, ServiceClientFactory) -> None
        """Input to Request Handler, Exception Handler and Interceptors.

        :param request_envelope: Request Envelope passed from Alexa
            Service.
        :type request_envelope: ask_sdk_model.request_envelope.RequestEnvelope
        :param attributes_manager: Attribute Manager instance for
            managing attributes across skill lifecycle
        :type attributes_manager:
            ask_sdk_core.attributes_manager.AttributesManager
        :param context: Context object passed from Lambda service
        :type context: object
        :param service_client_factory: Service Client Factory instance
            for calling Alexa services
        :type service_client_factory:
            ask_sdk_model.services.service_client_factory.ServiceClientFactory
        """
        self.request_envelope = request_envelope
        self.context = context
        self.service_client_factory = service_client_factory
        self.attributes_manager = attributes_manager
        self.response_builder = ResponseFactory()

    @property
    def service_client_factory(self):
        # type: () -> ServiceClientFactory
        """Service Client Factory instance for calling Alexa services.

        To use the Alexa services, one need to configure the API Client
        in the skill builder object, before creating the skill.
        """
        if self._service_client_factory is None:
            raise ValueError(
                "Attempting to use service client factory with no "
                "configured API client")

        return self._service_client_factory

    @service_client_factory.setter
    def service_client_factory(self, service_client_factory):
        # type: (ServiceClientFactory) -> None
        """
        :type service_client_factory: ask_sdk_model.services.
            ServiceClientFactory
        """
        self._service_client_factory = service_client_factory
