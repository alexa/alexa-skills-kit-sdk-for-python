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

from ..exceptions import DispatchException

if typing.TYPE_CHECKING:
    from typing import Union, List
    from ask_sdk_model import Response
    from ..handler_input import HandlerInput


class AbstractRequestHandler(object):
    """Request Handlers are responsible for processing Request inside
    the Handler Input and generating Response.

    Custom request handlers needs to implement ``can_handle`` and
    ``handle`` methods. ``can_handle`` returns True if the handler can
    handle the current request. ``handle`` processes the Request and
    may return a Response.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        """Returns true if Request Handler can handle the Request
        inside Handler Input.

        :param handler_input: Handler Input instance with
            Request Envelope containing Request.
        :type handler_input: HandlerInput
        :return: Boolean value that tells the dispatcher if the
            current request can be handled by this handler.
        :rtype: bool
        """
        pass

    @abstractmethod
    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]
        """Handles the Request inside handler input and provides a
        Response for dispatcher to return.

        :param handler_input: Handler Input instance with
            Request Envelope containing Request.
        :type handler_input: HandlerInput
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        pass


class AbstractRequestInterceptor(object):
    """Interceptor that runs before the handler is called.

    The ``process`` method has to be implemented, to run custom logic on
    the input, before it is handled by the Handler.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        """Process the input before the Handler is run.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :rtype: None
        """
        pass


class AbstractResponseInterceptor(object):
    """Interceptor that runs after the handler is called.

    The ``process`` method has to be implemented, to run custom logic on
    the input and the response generated after the handler is executed
    on the input.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        """Process the input and the response after the Handler is run.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :param response: Execution result of the Handler on
            handler input.
        :type response: Union[None, :py:class:`ask_sdk_model.Response`]
        :rtype: None
        """
        pass


class AbstractRequestHandlerChain(object):
    """Abstract class containing Request Handler and corresponding
    Interceptors.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def request_handler(self):
        # type: () -> object
        """

        :return: Registered Request Handler instance.
        :rtype: object
        """
        pass

    @abstractmethod
    def request_interceptors(self):
        # type: () -> List[AbstractRequestInterceptor]
        """
        :return: List of registered Request Interceptors.
        :rtype: list(AbstractRequestInterceptor)
        """
        pass

    @abstractmethod
    def response_interceptors(self):
        # type: () -> List[AbstractResponseInterceptor]
        """

        :return: List of registered Response Interceptors.
        :rtype: list(AbstractResponseInterceptor)
        """
        pass


class GenericRequestHandlerChain(AbstractRequestHandlerChain):
    """Generic implementation of
    :py:class:`AbstractRequestHandlerChain`.

    Generic Request Handler Chain accepts request handler of any type.
    This class can be used to register request handler of type other
    than :py:class:`AbstractRequestHandler`.

    :param request_handler: Registered Request Handler instance of
        generic type.
    :type request_handler: AbstractRequestHandler
    :param request_interceptors:  List of registered Request
        Interceptors.
    :type request_interceptors: list(AbstractRequestInterceptor)
    :param response_interceptors: List of registered Response
        Interceptors.
    :type response_interceptors: list(AbstractResponseInterceptor)
    """
    def __init__(
            self, request_handler, request_interceptors=None,
            response_interceptors=None):
        # type: (AbstractRequestHandler, List[AbstractRequestInterceptor], List[AbstractResponseInterceptor]) -> None
        """Generic implementation of
        :py:class:`AbstractRequestHandlerChain`.

        :param request_handler: Registered Request Handler instance of
            generic type.
        :type request_handler: AbstractRequestHandler
        :param request_interceptors:  List of registered Request
            Interceptors.
        :type request_interceptors: list(AbstractRequestInterceptor)
        :param response_interceptors: List of registered Response
            Interceptors.
        :type response_interceptors: list(AbstractResponseInterceptor)
        """
        self.request_handler = request_handler
        self.request_interceptors = request_interceptors
        self.response_interceptors = response_interceptors

    @property
    def request_handler(self):
        # type: () -> object
        return self._request_handler

    @request_handler.setter
    def request_handler(self, request_handler):
        # type: (AbstractRequestHandler) -> None
        if request_handler is None:
            raise DispatchException("No Request Handler provided")
        self._request_handler = request_handler

    @property
    def request_interceptors(self):
        # type: () -> List[AbstractRequestInterceptor]
        return self._request_interceptors

    @request_interceptors.setter
    def request_interceptors(self, request_interceptors):
        # type: (List[AbstractRequestInterceptor]) -> None
        if request_interceptors is None:
            request_interceptors = []
        self._request_interceptors = request_interceptors

    @property
    def response_interceptors(self):
        # type: () -> List[AbstractResponseInterceptor]
        return self._response_interceptors

    @response_interceptors.setter
    def response_interceptors(self, response_interceptors):
        # type: (List[AbstractResponseInterceptor]) -> None
        if response_interceptors is None:
            response_interceptors = []
        self._response_interceptors = response_interceptors

    def add_request_interceptor(self, interceptor):
        # type: (AbstractRequestInterceptor) -> None
        """Add interceptor to Request Interceptors list.

        :param interceptor: Request Interceptor instance.
        :type interceptor: AbstractRequestInterceptor
        """
        self.request_interceptors.append(interceptor)

    def add_response_interceptor(self, interceptor):
        # type: (AbstractResponseInterceptor) -> None
        """Add interceptor to Response Interceptors list.

        :param interceptor: Response Interceptor instance.
        :type interceptor: AbstractResponseInterceptor
        """
        self.response_interceptors.append(interceptor)


class RequestHandlerChain(GenericRequestHandlerChain):
    """Implementation of :py:class:`AbstractRequestHandlerChain` which
    handles :py:class:`AbstractRequestHandler`.

    :param request_handler: Registered Request Handler instance.
    :type request_handler: AbstractRequestHandler
    :param request_interceptors:  List of registered Request
        Interceptors.
    :type request_interceptors: list(AbstractRequestInterceptor)
    :param response_interceptors: List of registered Response
        Interceptors.
    :type response_interceptors: list(AbstractResponseInterceptor)
    :raises: :py:class:`ask_sdk_core.exceptions.DispatchException`
        when invalid request handler is provided.
    """

    def __init__(
            self, request_handler, request_interceptors=None,
            response_interceptors=None):
        # type: (AbstractRequestHandler, List[AbstractRequestInterceptor], List[AbstractResponseInterceptor]) -> None
        """Implementation of :py:class:`AbstractRequestHandlerChain`
        which handles :py:class:`AbstractRequestHandler`.

        :param request_handler: Registered Request Handler instance.
        :type request_handler: AbstractRequestHandler
        :param request_interceptors:  List of registered Request
            Interceptors.
        :type request_interceptors: list(AbstractRequestInterceptor)
        :param response_interceptors: List of registered Response
            Interceptors.
        :type response_interceptors: list(AbstractResponseInterceptor)
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException`
            when invalid request handler is provided.
        """
        if request_handler is None or not isinstance(
                request_handler, AbstractRequestHandler):
            raise DispatchException(
                "Invalid Request Handler provided. Expected "
                "Request Handler instance")

        super(RequestHandlerChain, self).__init__(
            request_handler=request_handler,
            request_interceptors=request_interceptors,
            response_interceptors=response_interceptors)

    @GenericRequestHandlerChain.request_handler.setter
    def request_handler(self, request_handler):
        # type: (AbstractRequestHandler) -> None
        if request_handler is None or not isinstance(
                request_handler, AbstractRequestHandler):
            raise DispatchException(
                "Invalid Request Handler provided. Expected "
                "Request Handler instance")

        GenericRequestHandlerChain.request_handler.fset(
            self, request_handler)


class AbstractRequestMapper(object):
    """Class for request routing to the appropriate handler chain.

    User needs to implement ``get_request_handler_chain`` method, to
    provide a routing mechanism of the input to the appropriate request
    handler chain containing the handler and the interceptors.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_request_handler_chain(self, handler_input):
        # type: (HandlerInput) -> AbstractRequestHandlerChain
        """Get the handler chain that can process the handler input.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :return: Handler Chain that can handle the request under
            handler input.
        :rtype: AbstractRequestHandlerChain
        """
        pass


class RequestMapper(AbstractRequestMapper):
    """Implementation of :py:class:`AbstractRequestMapper` that
    registers :py:class:`RequestHandlerChain`.

    The class accepts request handler chains of type
    :py:class:`RequestHandlerChain` only. The
    ``get_request_handler_chain`` method returns the
    :py:class:`RequestHandlerChain` instance that can
    handle the request in the handler input.

    :param request_handler_chains: List of
            :py:class:`RequestHandlerChain` instances.
    :type request_handler_chains: list(RequestHandlerChain)
    """

    def __init__(self, request_handler_chains):
        # type: (List[RequestHandlerChain]) -> None
        """Implementation of :py:class:`AbstractRequestMapper` that
        registers :py:class:`RequestHandlerChain`.

        The class accepts request handler chains of type
        :py:class:`RequestHandlerChain` only.

        :param request_handler_chains: List of
            :py:class:`RequestHandlerChain` instances.
        :type request_handler_chains: list(RequestHandlerChain)
        """
        self.request_handler_chains = request_handler_chains

    @property
    def request_handler_chains(self):
        # type: () -> List[RequestHandlerChain]
        """

        :return: List of :py:class:`RequestHandlerChain` instances.
        :rtype: list(RequestHandlerChain)
        """
        return self._request_handler_chains

    @request_handler_chains.setter
    def request_handler_chains(self, request_handler_chains):
        # type: (List[RequestHandlerChain]) -> None
        """

        :param request_handler_chains: List of
            :py:class:`RequestHandlerChain` instances.
        :type request_handler_chains: list(RequestHandlerChain)
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException`
            when any object inside the input list is of invalid type
        """
        self._request_handler_chains = []
        if request_handler_chains is not None:
            for chain in request_handler_chains:
                self.add_request_handler_chain(request_handler_chain=chain)

    def add_request_handler_chain(self, request_handler_chain):
        # type: (RequestHandlerChain) -> None
        """Checks the type before adding it to the
        request_handler_chains instance variable.

        :param request_handler_chain:  Request Handler Chain instance.
        :type request_handler_chain: RequestHandlerChain
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException`
            if a null input is provided or if the input is of invalid type
        """
        if request_handler_chain is None or not isinstance(
                request_handler_chain, RequestHandlerChain):
            raise DispatchException(
                "Request Handler Chain is not a RequestHandlerChain instance")
        self._request_handler_chains.append(request_handler_chain)

    def get_request_handler_chain(self, handler_input):
        # type: (HandlerInput) -> Union[RequestHandlerChain, None]
        """Get the request handler chain that can handle the input.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :return: Handler Chain that can handle the input.
        :rtype: Union[None, RequestHandlerChain]
        """
        for chain in self.request_handler_chains:
            handler = chain.request_handler
            if handler.can_handle(handler_input=handler_input):
                return chain
        return None


class AbstractHandlerAdapter(object):
    """Abstracts handling of a request for specific handler types."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def supports(self, handler):
        # type: (AbstractRequestHandler) -> bool
        """Returns true if adapter supports the handler.

        This method checks if the adapter supports the handler
        execution. This is usually checked by the type of the handler.

        :param handler: Request Handler instance.
        :type handler: object
        :return: Boolean denoting whether the adapter supports the
            handler.
        :rtype: bool
        """
        pass

    @abstractmethod
    def execute(self, handler_input, handler):
        # type: (HandlerInput, AbstractRequestHandler) -> Union[None, Response]
        """Executes the handler with the provided handler input.

        :param handler_input: Input containing request envelope,
            context and other fields for request handling.
        :type handler_input: HandlerInput
        :param handler: Request Handler instance.
        :type handler: object
        :return: Result executed by passing handler_input to handler.
        :rtype: Union[None, Response]
        """
        pass


class HandlerAdapter(AbstractHandlerAdapter):
    """Handler Adapter for handlers of type
    :py:class:`AbstractRequestHandler`.
    """

    def supports(self, handler):
        # type: (AbstractRequestHandler) -> bool
        """Returns true if handler is
        :py:class:`AbstractRequestHandler` instance.

        :param handler: Request Handler instance
        :type handler: AbstractRequestHandler
        :return: Boolean denoting whether the adapter supports the
            handler.
        :rtype: bool
        """
        return isinstance(handler, AbstractRequestHandler)

    def execute(self, handler_input, handler):
        # type: (HandlerInput, AbstractRequestHandler) -> Union[None, Response]
        """Executes the handler with the provided handler input.

        :param handler_input: Input containing request envelope,
            context and other fields for request handling.
        :type handler_input: HandlerInput
        :param handler: Request Handler instance.
        :type handler: object
        :return: Result executed by passing handler_input to handler.
        :rtype: Union[None, Response]
        """
        return handler.handle(handler_input)
