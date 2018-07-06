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
from abc import ABCMeta, abstractmethod

from .exceptions import DispatchException

if typing.TYPE_CHECKING:
    from typing import Union, List
    from ask_sdk_model import Response
    from .handler_input import HandlerInput
    from .dispatch_components import (
        HandlerAdapter, RequestMapper, ExceptionMapper,
        AbstractRequestInterceptor, AbstractResponseInterceptor)


class AbstractRequestDispatcher(object):
    """Dispatcher which handles dispatching input request to the
    corresponding handler.

    User needs to implement the dispatch method, to handle the
    processing of the incoming request in the handler input. A response
    may be expected out of the dispatch method. User also has the
    flexibility of processing invalid requests by raising custom
    exceptions wrapped under
    :py:class:`ask_sdk_core.exceptions.DispatchException`.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def dispatch(self, handler_input):
        # type: (HandlerInput) -> Union[Response, None]
        """Dispatches an incoming request to the appropriate request
        handler and returns the output.

        :param handler_input: input to the dispatcher containing
            incoming request and other context
        :type handler_input: HandlerInput
        :return: output optionally containing a response
        :rtype: Union[None, Response]
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException`
        """
        pass


class RequestDispatcher(AbstractRequestDispatcher):
    """Default implementation of :py:class:`AbstractRequestDispatcher`.

    When the dispatch method is invoked, using a list of
    :py:class:`ask_sdk_core.dispatch_components.request_components.RequestMapper`
    , the Dispatcher finds a handler for the request and delegates the
    invocation to the supported
    :py:class:`ask_sdk_core.dispatch_components.request_components.HandlerAdapter`
    . If the handler raises any exception, it is delegated to
    :py:class:`ask_sdk_core.dispatch_components.exception_components.ExceptionMapper`
    to handle or raise it to the upper stack.

    :param handler_adapters: List of handler adapters that are
            supported by the dispatcher.
    :type handler_adapters: list[HandlerAdapter]
    :param request_mappers: List of Request Mappers containing
        user defined handlers.
    :type request_mappers: list[RequestMapper]
    :param exception_mapper: Exception mapper containing custom
        exception handlers.
    :type exception_mapper: ExceptionMapper
    :param request_interceptors: List of Request Interceptors
    :type request_interceptors: list[AbstractRequestInterceptor]
    :param response_interceptors: List of Response Interceptors
    :type response_interceptors: list[AbstractResponseInterceptor]
    """

    def __init__(
            self, handler_adapters=None, request_mappers=None,
            exception_mapper=None, request_interceptors=None,
            response_interceptors=None):
        # type: (List[HandlerAdapter], List[RequestMapper], ExceptionMapper, List[AbstractRequestInterceptor], List[AbstractResponseInterceptor]) -> None
        """Default implementation of :py:class:`RequestDispatcher`.

        :param handler_adapters: List of handler adapters that are
            supported by the dispatcher.
        :type handler_adapters: list[HandlerAdapter]
        :param request_mappers: List of Request Mappers containing
            user defined handlers.
        :type request_mappers: list[RequestMapper]
        :param exception_mapper: Exception mapper containing custom
            exception handlers.
        :type exception_mapper: ExceptionMapper
        :param request_interceptors: List of Request Interceptors
        :type request_interceptors: list[AbstractRequestInterceptor]
        :param response_interceptors: List of Response Interceptors
        :type response_interceptors: list[AbstractResponseInterceptor]
        """
        if handler_adapters is None:
            handler_adapters = []

        if request_mappers is None:
            request_mappers = []

        if request_interceptors is None:
            request_interceptors = []

        if response_interceptors is None:
            response_interceptors = []

        self.handler_adapters = handler_adapters
        self.request_mappers = request_mappers
        self.exception_mapper = exception_mapper
        self.request_interceptors = request_interceptors
        self.response_interceptors = response_interceptors

    def dispatch(self, handler_input):
        # type: (HandlerInput) -> Union[Response, None]
        """Dispatches an incoming request to the appropriate
        request handler and returns the output.

        Before running the request on the appropriate request handler,
        dispatcher runs any predefined global request interceptors.
        On successful response returned from request handler, dispatcher
        runs predefined global response interceptors, before returning
        the response.

        :param handler_input: input to the dispatcher containing
            incoming request and other context
        :type handler_input: HandlerInput
        :return: output optionally containing a response
        :rtype: Union[None, Response]
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException`
        """
        try:
            for request_interceptor in self.request_interceptors:
                request_interceptor.process(handler_input=handler_input)

            response = self.__dispatch_request(handler_input)

            for response_interceptor in self.response_interceptors:
                response_interceptor.process(
                    handler_input=handler_input, response=response)

            return response
        except Exception as e:
            if self.exception_mapper is not None:
                exception_handler = self.exception_mapper.get_handler(
                    handler_input, e)
                if exception_handler is None:
                    raise e
                return exception_handler.handle(handler_input, e)
            else:
                raise e

    def __dispatch_request(self, handler_input):
        # type: (HandlerInput) -> Union[Response, None]
        """Process the request in handler input and return
        handler output.

        When the method is invoked, using the registered list of
        :py:class:`RequestMapper`, a Handler Chain is found that can
        handle the request. The handler invocation is delegated to the
        supported :py:class:`HandlerAdapter`. The registered
        request interceptors in the handler chain are processed before
        executing the handler. The registered response interceptors in
        the handler chain are processed after executing the handler.

        :param handler_input: input to the dispatcher containing
            incoming request and other context.
        :type handler_input: HandlerInput
        :return: Output from the 'handle' method execution of the
            supporting handler.
        :rtype: Union[None, Response]
        :raises DispatchException if there is no supporting
            handler chain or adapter
        """
        request_handler_chain = None
        for mapper in self.request_mappers:
            request_handler_chain = mapper.get_request_handler_chain(
                handler_input)
            if request_handler_chain is not None:
                break

        if request_handler_chain is None:
            raise DispatchException(
                "Couldn't find handler that can handle the "
                "request: {}".format(handler_input.request_envelope.request))

        request_handler = request_handler_chain.request_handler
        supported_handler_adapter = None
        for adapter in self.handler_adapters:
            if adapter.supports(request_handler):
                supported_handler_adapter = adapter
                break

        if supported_handler_adapter is None:
            raise DispatchException(
                "Couldn't find adapter that can handle the "
                "request: {}".format(handler_input.request_envelope.request))

        local_request_interceptors = request_handler_chain.request_interceptors
        for interceptor in local_request_interceptors:
            interceptor.process(handler_input=handler_input)

        response = supported_handler_adapter.execute(
            handler_input=handler_input, handler=request_handler)

        local_response_interceptors = (
            request_handler_chain.response_interceptors)
        for interceptor in local_response_interceptors:
            interceptor.process(handler_input=handler_input, response=response)

        return response
