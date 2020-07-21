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

if typing.TYPE_CHECKING:
    from typing import Dict


class WebSocketConfiguration(object):
    """Configuration class for web-socket connection. Allows the
    connection URI and request with headers to be configured.
    """

    def __init__(self, web_socket_server_uri, headers):
        # type: (str, Dict[str, str]) -> None
        """Configuration class for web-socket connection. Allows the
        connection URI and request headers to be configured.

        :param web_socket_server_uri: URI required for websocket connection.
        :type web_socket_server_uri: str
        :param headers: Headers passed during debug connection request.
        :type headers: Dict[str, str]
        """
        self.web_socket_server_uri = web_socket_server_uri
        self.headers = headers
