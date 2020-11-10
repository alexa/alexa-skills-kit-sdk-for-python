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

from ask_sdk_local_debug.config.skill_invoker_config import SkillInvokerConfiguration
from ask_sdk_local_debug.config.client_config import ClientConfiguration
from ask_sdk_local_debug.config.websocket_config import WebSocketConfiguration
from ask_sdk_local_debug.client.autobahn_client import AutobahnClient
from ask_sdk_local_debug.config.region import Region
from ask_sdk_local_debug.exception import LocalDebugSdkException

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    import argparse

# Upgrade header value.
UPGRADE_HEADER_VALUE = "websocket"
# Upgrade header key.
UPGRADE_HEADER_NAME = "upgrade"
# Connection header key.
CONNECTION_HEADER_NAME = "connection"
# Connection header value.
CONNECTION_HEADER_VALUE = "upgrade"
# Authorization header key.
AUTHORIZATION_HEADER_NAME = "authorization"
# Web socket connection uri skeleton.
# TODO: Update to prod endpoint URL.
DEBUG_ENDPOINT_URI = "wss://{}/v1/skills/{}/stages/development/connectCustomDebugEndpoint"


def create_web_socket_client(parsed_args):
    # type: (argparse.Namespace) -> AutobahnClient
    """Create websocket client instance with parsed debug config parameters.

    :param parsed_args: Parsed parameter object returned from
        parser.argument_parser function.
    :type parsed_args: object
    :return: WebSocketClient instance.
    :rtype: :py:class:`ask_sdk_local_debug.client.AutobahnClient`
    """
    web_socket_config = create_web_socket_configuration(parsed_args)
    skill_invoker_config = create_skill_invoker_config(parsed_args)

    return AutobahnClient(web_socket_config, skill_invoker_config)


def create_web_socket_configuration(parsed_args):
    # type: (argparse.Namespace) -> WebSocketConfiguration
    """Create websocket configuration instance with parsed debug config
    parameters.

    WebSocket configures the server URI used to connect for local debug session
    and sets the headers information for initial handshake of sockets and
    authorization of clients.

    :param parsed_args: Parsed parameter object returned from
        parser.argument_parser function.
    :type parsed_args: object
    :return: WebSocketConfiguration instance.
    :rtype: :py:class:`ask_sdk_local_debug.config.WebSocketConfiguration`
    """
    client_config = create_client_configuration(parsed_args)
    access_token = parsed_args.access_token
    if parsed_args.region not in list(Region.__members__):
        error_message = "Invalid region - {}. Please ensure that the region value is one of " \
                        "{}".format(parsed_args.region, list(Region.__members__))
        logger.error(error_message)
        raise LocalDebugSdkException(error_message)
    logger.info("Region chosen: " + parsed_args.region)
    debug_endpoint_uri = DEBUG_ENDPOINT_URI.format(Region[parsed_args.region].value, client_config.skill_id)

    headers = {AUTHORIZATION_HEADER_NAME: access_token,
               UPGRADE_HEADER_NAME: UPGRADE_HEADER_VALUE,
               CONNECTION_HEADER_NAME: CONNECTION_HEADER_VALUE}
    return WebSocketConfiguration(web_socket_server_uri=debug_endpoint_uri,
                                  headers=headers)


def create_client_configuration(parsed_args):
    # type: (argparse.Namespace) -> ClientConfiguration
    """Create client configuration instance with parsed debug config
    parameters.

    :param parsed_args: Parsed parameter object returned from
        parser.argument_parser function.
    :type parsed_args: object
    :return: Client Configuration object
    :rtype: :py:class:`ask_sdk_local_debug.config.ClientConfiguration`
    """

    return ClientConfiguration(access_token=parsed_args.access_token,
                               skill_id=parsed_args.skill_id,
                               skill_file_path=parsed_args.skill_file_path,
                               skill_handler=parsed_args.skill_handler)


def create_skill_invoker_config(parsed_args):
    # type: (argparse.Namespace) -> SkillInvokerConfiguration
    """Create a skill skill_invoker_config configuration instance with parsed debug config
    parameters.

    :param parsed_args: Parsed parameter object returned from
        parser.argument_parser function.
    :type parsed_args: object
    :return: Skill Invoker Configuration object.
    :rtype: :py:class:`ask_sdk_local_debug.config.SkillInvokerConfiguration`
    """
    return SkillInvokerConfiguration(
        skill_file_path=parsed_args.skill_file_path,
        skill_handler=parsed_args.skill_handler)
