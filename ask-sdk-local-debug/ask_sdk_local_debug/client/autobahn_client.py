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
import logging

from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, connectWS

from ask_sdk_local_debug.client.abstract_websocket_client import AbstractWebSocketClient
from ask_sdk_local_debug.client.autobahn_client_protocol import AutobahnClientProtocol
from ask_sdk_local_debug.config.constant_config import CONNECTION_TIMEOUT_SECONDS, PING_INTERVAL_SECONDS
from ask_sdk_local_debug.exception import LocalDebugSdkException

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from ask_sdk_local_debug.config.skill_invoker_config import SkillInvokerConfiguration
    from ask_sdk_local_debug.config.websocket_config import WebSocketConfiguration


class AutobahnClientFactory(WebSocketClientFactory):
    """WebSocketClientFactory to set the client protocol and log socket
    connection failures."""

    protocol = AutobahnClientProtocol

    def startedConnecting(self, connector):
        logger.info("Initiating webSocket connection.")

    def clientConnectionLost(self, connector, reason):
        logger.error('Connection Lost. Reason: {}'.format(
            reason.getErrorMessage()))

    def clientConnectionFailed(self, connector, reason):
        logger.error('Connection failed. Reason: {}'.format(
            reason.getErrorMessage()))


class AutobahnClient(AbstractWebSocketClient):
    """Web socket client wrapper re-purposed for local debugging."""

    def __init__(self, web_socket_config, skill_invoker_config):
        # type: (WebSocketConfiguration, SkillInvokerConfiguration) -> None
        """Initialize the Autobahn websocket client instance.

        :param web_socket_config: Web Socket client configuration class.
        :type web_socket_config: :py:class:`ask_sdk_local_debug.config.WebSocketConfiguration`
        :param skill_invoker_config: Skill Invoker Config instance to invoke
            skill code.
        :type skill_invoker_config: :py:class:`ask_sdk_local_debug.skill_invoker_config.SkillInvokerConfiguration`
        """
        self.web_socket_config = web_socket_config
        self.factory = AutobahnClientFactory(
            self.web_socket_config.web_socket_server_uri,
            headers=self.web_socket_config.headers)
        self.factory.setProtocolOptions(autoPingInterval=PING_INTERVAL_SECONDS,
                                        autoPingTimeout=CONNECTION_TIMEOUT_SECONDS)
        self.factory.skill_invoker_config = skill_invoker_config

    def invoke(self):
        # type: () -> None
        """Triggers the web socket client to make a connection attempt
        on the provided websocket uri.
        """
        try:
            connectWS(self.factory, contextFactory=None, timeout=CONNECTION_TIMEOUT_SECONDS)
            reactor.run()
        except Exception as e:
            logger.error(
                'Unable to initiate a socket client connection : {}'.format(
                    str(e)))
            raise LocalDebugSdkException(
                "Unable to initiate a socket client connection : {}".format(
                    str(e)))
