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
import json
import typing

from ask_sdk_model import RequestEnvelope

from .dispatch_components import (
    AbstractRequestHandler, RequestHandlerChain, RequestMapper,
    HandlerAdapter, AbstractRequestInterceptor, AbstractResponseInterceptor,
    ExceptionMapper, AbstractExceptionHandler)
from .skill import Skill, SkillConfiguration
from .exceptions import SkillBuilderException


if typing.TYPE_CHECKING:
    from typing import Callable, TypeVar, Dict
    from ask_sdk_model.services import ApiClient
    from .handler_input import HandlerInput
    from .attributes_manager import AbstractPersistenceAdapter
    T = TypeVar('T')


class SkillBuilder(object):
    """Skill Builder with helper functions for building
    :py:class:`Skill` object.
    """

    def __init__(self):
        # type: () -> None
        self.request_handlers = []
        self.exception_handlers = []
        self.global_request_interceptors = []
        self.global_response_interceptors = []
        self.custom_user_agent = None
        self.skill_id = None

    @property
    def skill_configuration(self):
        # type: () -> SkillConfiguration
        """Create the skill configuration object using the
        registered components.
        """
        request_handler_chains = []

        for handler in self.request_handlers:
            request_handler_chains.append(
                RequestHandlerChain(request_handler=handler))

        request_mapper = RequestMapper(
            request_handler_chains=request_handler_chains)

        if self.exception_handlers:
            exception_mapper = ExceptionMapper(
                exception_handlers=self.exception_handlers)
        else:
            exception_mapper = None

        return SkillConfiguration(
            request_mappers=[request_mapper],
            handler_adapters=[HandlerAdapter()],
            exception_mapper=exception_mapper,
            request_interceptors=self.global_request_interceptors,
            response_interceptors=self.global_response_interceptors,
            custom_user_agent=self.custom_user_agent,
            skill_id=self.skill_id
        )

    def add_request_handler(self, request_handler):
        # type: (AbstractRequestHandler) -> None
        """Register input to the request handlers list.

        :param request_handler: Request Handler instance to be
            registered.
        :type request_handler: AbstractRequestHandler
        :return: None
        """
        if request_handler is None:
            raise SkillBuilderException(
                "Valid Request Handler instance to be provided")

        if not isinstance(request_handler, AbstractRequestHandler):
            raise SkillBuilderException(
                "Input should be a RequestHandler instance")

        self.request_handlers.append(request_handler)

    def add_exception_handler(self, exception_handler):
        # type: (AbstractExceptionHandler) -> None
        """Register input to the exception handlers list.

        :param exception_handler: Exception Handler instance to be
            registered.
        :type exception_handler: AbstractExceptionHandler
        :return: None
        """
        if exception_handler is None:
            raise SkillBuilderException(
                "Valid Exception Handler instance to be provided")

        if not isinstance(exception_handler, AbstractExceptionHandler):
            raise SkillBuilderException(
                "Input should be an ExceptionHandler instance")

        self.exception_handlers.append(exception_handler)

    def add_global_request_interceptor(self, request_interceptor):
        # type: (AbstractRequestInterceptor) -> None
        """Register input to the global request interceptors list.

        :param request_interceptor: Request Interceptor instance to be
            registered.
        :type request_interceptor: AbstractRequestInterceptor
        :return: None
        """
        if request_interceptor is None:
            raise SkillBuilderException(
                "Valid Request Interceptor instance to be provided")

        if not isinstance(request_interceptor, AbstractRequestInterceptor):
            raise SkillBuilderException(
                "Input should be a RequestInterceptor instance")

        self.global_request_interceptors.append(request_interceptor)

    def add_global_response_interceptor(self, response_interceptor):
        # type: (AbstractResponseInterceptor) -> None
        """Register input to the global response interceptors list.

        :param response_interceptor: Response Interceptor instance to
            be registered.
        :type response_interceptor: AbstractResponseInterceptor
        :return: None
        """
        if response_interceptor is None:
            raise SkillBuilderException(
                "Valid Response Interceptor instance to be provided")

        if not isinstance(response_interceptor, AbstractResponseInterceptor):
            raise SkillBuilderException(
                "Input should be a ResponseInterceptor instance")

        self.global_response_interceptors.append(response_interceptor)

    def create(self):
        # type: () -> Skill
        """Create a skill object using the registered components.

        :return: a skill object that can be used for invocation.
        :rtype: Skill
        """
        return Skill(skill_configuration=self.skill_configuration)

    def lambda_handler(self):
        # type: () -> Callable[[RequestEnvelope, T], Dict[str, T]]
        """Create a handler function that can be used as handler in
        AWS Lambda console.

        The lambda handler provides a handler function, that acts as
        an entry point to the AWS Lambda console. Users can set the
        lambda_handler output to a variable and set the variable as
        AWS Lambda Handler on the console.

        :return: Handler function to tag on AWS Lambda console.
        """
        def wrapper(event, context):
            # type: (RequestEnvelope, T) -> Dict[str, T]
            skill = Skill(skill_configuration=self.skill_configuration)
            request_envelope = skill.serializer.deserialize(
                payload=json.dumps(event), obj_type=RequestEnvelope)
            response_envelope = skill.invoke(
                request_envelope=request_envelope, context=context)
            return skill.serializer.serialize(response_envelope)
        return wrapper

    def request_handler(self, can_handle_func):
        # type: (Callable[[HandlerInput], bool]) -> Callable
        """Decorator that can be used to add request handlers easily to
        the builder.

        The can_handle_func has to be a Callable instance, which takes
        a single parameter and no varargs or kwargs. This is because
        of the RequestHandler class signature restrictions. The
        returned wrapper function can be applied as a decorator on any
        function that returns a response object by the skill. The
        function should follow the signature of the handle function in
        :py:class:`ask_sdk_core.dispatch_components.request_components.AbstractRequestHandler`
        class.

        :param can_handle_func: The function that validates if the
            request can be handled.
        :type can_handle_func: Callable[[HandlerInput], bool]
        :return: Wrapper function that can be decorated on a handle
            function.
        """
        def wrapper(handle_func):
            if not callable(can_handle_func) or not callable(handle_func):
                raise SkillBuilderException(
                    "Request Handler can_handle_func and handle_func "
                    "input parameters should be callable")

            class_attributes = {
                "can_handle": lambda self, handler_input: can_handle_func(
                    handler_input),
                "handle": lambda self, handler_input: handle_func(
                    handler_input)
            }

            request_handler_class = type(
                "RequestHandler{}".format(
                    handle_func.__name__.title().replace("_", "")),
                (AbstractRequestHandler,), class_attributes)

            self.add_request_handler(request_handler=request_handler_class())
        return wrapper

    def exception_handler(self, can_handle_func):
        # type: (Callable[[HandlerInput, Exception], bool]) -> Callable
        """Decorator that can be used to add exception handlers easily
        to the builder.

        The can_handle_func has to be a Callable instance, which takes
        two parameters and no varargs or kwargs. This is because of the
        ExceptionHandler class signature restrictions. The returned
        wrapper function can be applied as a decorator on any function
        that processes the exception raised during dispatcher and
        returns a response object by the skill. The function should
        follow the signature of the handle function in
        :py:class:`ask_sdk_core.dispatch_components.exception_components.AbstractExceptionHandler`
        class.

        :param can_handle_func: The function that validates if the
            exception can be handled.
        :type can_handle_func: Callable[[HandlerInput, Exception], bool]
        :return: Wrapper function that can be decorated on a handle
            function.
        """
        def wrapper(handle_func):
            if not callable(can_handle_func) or not callable(handle_func):
                raise SkillBuilderException(
                    "Exception Handler can_handle_func and handle_func input "
                    "parameters should be callable")

            class_attributes = {
                "can_handle": (
                    lambda self, handler_input, exception: can_handle_func(
                        handler_input, exception)),
                "handle": lambda self, handler_input, exception: handle_func(
                    handler_input, exception)
            }

            exception_handler_class = type(
                "ExceptionHandler{}".format(
                    handle_func.__name__.title().replace("_", "")),
                (AbstractExceptionHandler,), class_attributes)

            self.add_exception_handler(
                exception_handler=exception_handler_class())
        return wrapper

    def global_request_interceptor(self):
        # type: () -> Callable
        """Decorator that can be used to add global request
        interceptors easily to the builder.

        The returned wrapper function can be applied as a decorator on
        any function that processes the input. The function should
        follow the signature of the process function in
        :py:class:`ask_sdk_core.dispatch_components.request_components.AbstractRequestInterceptor`
        class.

        :return: Wrapper function that can be decorated on a
            interceptor process function.
        """
        def wrapper(process_func):
            if not callable(process_func):
                raise SkillBuilderException(
                    "Global Request Interceptor process_func input parameter "
                    "should be callable")

            class_attributes = {
                "process": lambda self, handler_input: process_func(
                    handler_input)
            }

            request_interceptor = type(
                "RequestInterceptor{}".format(
                    process_func.__name__.title().replace("_", "")),
                (AbstractRequestInterceptor,), class_attributes)

            self.add_global_request_interceptor(
                request_interceptor=request_interceptor())
        return wrapper

    def global_response_interceptor(self):
        # type: () -> Callable
        """Decorator that can be used to add global
        response interceptors easily to the builder.

        The returned wrapper function can be applied as a decorator
        on any function that processes the input and the response
        generated by the request handler. The function should follow
        the signature of the process function in
        :py:class:`ask_sdk_core.dispatch_components.request_components.AbstractResponseInterceptor`
        class.

        :return: Wrapper function that can be decorated on a
            interceptor process function.
        """
        def wrapper(process_func):
            if not callable(process_func):
                raise SkillBuilderException(
                    "Global Response Interceptor process_func input "
                    "parameter should be callable")

            class_attributes = {
                "process": (
                    lambda self, handler_input, response: process_func(
                        handler_input, response))
            }

            response_interceptor = type(
                "ResponseInterceptor{}".format(
                    process_func.__name__.title().replace("_", "")),
                (AbstractResponseInterceptor,), class_attributes)

            self.add_global_response_interceptor(
                response_interceptor=response_interceptor())
        return wrapper


class CustomSkillBuilder(SkillBuilder):
    """Skill Builder with api client and persistence adapter setter
    functions.
    """

    def __init__(self, persistence_adapter=None, api_client=None):
        # type: (AbstractPersistenceAdapter, ApiClient) -> None
        """Skill Builder with api client and persistence adapter
        setter functions.
        """
        super(CustomSkillBuilder, self).__init__()
        self.persistence_adapter = persistence_adapter
        self.api_client = api_client

    @property
    def skill_configuration(self):
        # type: () -> SkillConfiguration
        """Create the skill configuration object using the
        registered components.
        """
        skill_config = super(CustomSkillBuilder, self).skill_configuration
        skill_config.persistence_adapter = self.persistence_adapter
        skill_config.api_client = self.api_client
        return skill_config
