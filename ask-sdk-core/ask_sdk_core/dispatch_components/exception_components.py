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


class AbstractExceptionHandler(object):
    """Handles exception types and optionally produce a response.

    The abstract class is similar to Request Handler, with methods
    can_handle and handle. The ``can_handle`` method checks if the handler
    can support the input and the exception. The ``handle`` method
    processes the input and exception, to optionally produce a response.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        """Checks if the handler can support the exception raised
        during dispatch.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :param exception: Exception raised during dispatch.
        :type exception: Exception
        :return: Boolean whether handler can handle exception or not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Union[Response, None]
        """Process the handler input and exception.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :param exception: Exception raised during dispatch.
        :type exception: Exception
        :return: Optional response object to serve as dispatch return.
        :rtype: Union[None, Response]
        """
        pass


class AbstractExceptionMapper(object):
    """Mapper to register custom Exception Handler instances.

    The exception mapper is used by
    :py:class:`ask_sdk_core.dispatch.RequestDispatcher`
    dispatch method, to handle exceptions. The mapper can contain one
    or more exception handlers. Handlers are accessed through the
    mapper to attempt to find a handler that is compatible with the
    current exception.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_handler(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Union[AbstractExceptionHandler, None]
        """Returns a suitable exception handler to dispatch the
        specified exception, if one exists.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :param exception: Exception thrown by
            :py:class:`ask_sdk_core.dispatch.RequestDispatcher` dispatch
            method.
        :type exception: Exception
        :return: Exception Handler that can handle the input or None.
        :rtype: Union[None, AbstractExceptionHandler]
        """
        pass


class ExceptionMapper(AbstractExceptionMapper):
    """Implementation of exception mapper, to register
    :py:class:`AbstractExceptionHandler` instances.

    The class accepts exception handlers of type
    :py:class:`AbstractExceptionHandler` only. The ``get_handler`` method
    returns the :py:class:`AbstractExceptionHandler` instance that can
    handle the handler input and the exception raised from the dispatch method.

    :param exception_handlers: List of
        :py:class:`AbstractExceptionHandler` instances.
    :type exception_handlers: list(AbstractExceptionHandler)
    """

    def __init__(self, exception_handlers):
        # type: (List[AbstractExceptionHandler]) -> None
        """Implementation of :py:class:`AbstractExceptionMapper` that
        registers :py:class:`AbstractExceptionHandler`.

        The class accepts exception handlers of type
        :py:class:`AbstractExceptionHandler` only.

        :param exception_handlers: List of
            :py:class:`AbstractExceptionHandler` instances.
        :type exception_handlers: list(AbstractExceptionHandler)
        """
        self.exception_handlers = exception_handlers

    @property
    def exception_handlers(self):
        # type: () -> List[AbstractExceptionHandler]
        """
        :return: List of :py:class:`AbstractExceptionHandler` instances.
        :rtype: list(AbstractExceptionHandler)
        """
        return self._exception_handlers

    @exception_handlers.setter
    def exception_handlers(self, exception_handlers):
        # type: (List[AbstractExceptionHandler]) -> None
        """

        :param exception_handlers: List of
            :py:class:`AbstractExceptionHandler` instances.
        :type exception_handlers: list(AbstractExceptionHandler)
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException` when
            any object inside the input list is of invalid type
        """
        self._exception_handlers = []
        if exception_handlers is not None:
            for handler in exception_handlers:
                self.add_exception_handler(exception_handler=handler)

    def add_exception_handler(self, exception_handler):
        # type: (AbstractExceptionHandler) -> None
        """Checks the type before adding it to the exception_handlers
        instance variable.

        :param exception_handler: Exception Handler instance.
        :type exception_handler: AbstractExceptionHandler
        :raises: :py:class:`ask_sdk_core.exceptions.DispatchException` if a
            null input is provided or if the input is of invalid type
        """
        if exception_handler is None or not isinstance(
                exception_handler, AbstractExceptionHandler):
            raise DispatchException(
                "Input is not an AbstractExceptionHandler instance")
        self._exception_handlers.append(exception_handler)

    def get_handler(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Union[AbstractExceptionHandler, None]
        """Get the exception handler that can handle the input and
        exception.

        :param handler_input: Handler Input instance.
        :type handler_input: HandlerInput
        :param exception: Exception thrown by
            :py:class:`ask_sdk_core.dispatch.RequestDispatcher` dispatch
            method.
        :type exception: Exception
        :return: Exception Handler that can handle the input or None.
        :rtype: Union[None, AbstractExceptionHandler]
        """
        for handler in self.exception_handlers:
            if handler.can_handle(
                    handler_input=handler_input, exception=exception):
                return handler
        return None
