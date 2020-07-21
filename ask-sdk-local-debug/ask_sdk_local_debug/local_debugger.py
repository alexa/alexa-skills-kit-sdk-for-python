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
import typing
from abc import abstractmethod, ABC

if typing.TYPE_CHECKING:
    from ask_sdk_local_debug.client.abstract_websocket_client import AbstractWebSocketClient


class AbstractLocalDebugger(ABC):
    """Abstract Class to represent Local Debugger.

    User needs to implement ``invoke`` method to invoke web-socket client.
    """
    @abstractmethod
    def invoke(self):
        pass


class LocalDebugger(AbstractLocalDebugger):
    """Setup Local Debugger client to invoke web-socket connection.

    Local debugger invokes the underlying implemented websocket client to
    setup the connection for debug session.
    """

    def __init__(self, web_socket_client):
        # type: (AbstractWebSocketClient) -> None
        """Setup Local Debugger client to invoke web-socket connection.

        Local debugger invokes the underlying implemented websocket client to
        setup the connection for debug session.
        """
        self.web_socket_client = web_socket_client

    def invoke(self):
        # type: () -> None
        """Invokes the :py:class:`ask_sdk_local_debug.client.WebSocketClient`
        class  ``invoke`` method for debugging.
        """
        self.web_socket_client.invoke()
