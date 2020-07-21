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
import json
import logging
import typing

from autobahn.twisted.websocket import WebSocketClientProtocol
from twisted.internet import reactor

from ask_sdk_local_debug.util.response_util import (get_skill_response,
                                                    get_deserialized_request)

logger = logging.getLogger(__name__)


if typing.TYPE_CHECKING:
    from autobahn.websocket.protocol import ConnectionResponse


class AutobahnClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        # type: (ConnectionResponse) -> None
        """Callback fired directly after web-socket opening handshake when new
        web-socket server connection was established.

        :param response: web-socket connection response information.
        :type response: instance of
        :py:class:`autobahn_client.websocket.protocol.ConnectionResponse`
        """
        logger.info("*****Starting Skill Debug Session*****")
        logger.info('*****Session will last for 1 hour*****')

    def onOpen(self):
        # type: () -> None
        """Callback fired directly after web-socket connection is
        established.
        """
        logger.info("Connection is open.")

    def onMessage(self, skill_request_payload, is_binary):
        # type: (bytes, bool) -> None
        """Callback fired when a complete web-socket message was received.

        :param skill_request_payload: The WebSocket message received.
        :type skill_request_payload: bytes

        :param is_binary: Flag indicating whether payload is binary or
            UTF-8 encoded text.
        :type is_binary: bool
        """
        decoded_payload = skill_request_payload.decode('utf8')
        logger.info("Skill request : \n {}".format(json.dumps(json.loads(decoded_payload), indent=4, sort_keys=True)))
        skill_request = get_deserialized_request(
            skill_request_payload=decoded_payload)
        skill_response = get_skill_response(
            local_debug_request=skill_request,
            skill_invoker_config=self.factory.skill_invoker_config)
        self.send_skill_response(local_debug_ask_response=skill_response)

    def onClose(self, was_clean, code, reason):
        # type: (bool, int, str) -> None
        """Callback fired when the WebSocket connection has been closed
        (WebSocket closing handshake has been finished or the connection was
        closed uncleanly).

        :param was_clean: ``True`` if the WebSocket connection was closed
        cleanly.
        :type was_clean: bool

        :param code: Close status code as sent by the WebSocket peer.
        :type code: int or None

        :param reason: Close reason as sent by the WebSocket peer.
        :type reason: str or None
        """
        logger.info("WebSocket connection closed: {} ".format(reason))
        reactor.stop()

    def send_skill_response(self, local_debug_ask_response):
        # type: (str) -> None
        """Sends skill response over the established web-socket connection.

        :param local_debug_ask_response: Sends response of the serialized
        :py:class:`ask_sdk_model.dynamicEndpoints.SuccessResponse` or
        :py:class:`ask_sdk_model.dynamicEndpoints.FailureResponse` over the
        established web-socket connection.
        :type local_debug_ask_response: str
        """
        logger.info(
            "Skill response: \n {}".format(json.dumps(json.loads(local_debug_ask_response), indent=4, sort_keys=True)))
        encoded_message = local_debug_ask_response.encode('utf8')
        self.sendMessage(encoded_message)
