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
import sys
import typing

from ask_sdk_local_debug.local_debugger import LocalDebugger
from ask_sdk_local_debug.util.parser import argument_parser
from ask_sdk_local_debug.util.websocket_util import create_web_socket_client

if typing.TYPE_CHECKING:
    from typing import List


class LocalDebuggerInvoker(object):
    """Initializing the LocalDebugger Invoker by setting up WebSocketClient
     and SkillInvokerConfigurations based on passed cmd arguments.

     This class is the main method invoked by the debugger configuration.
     Bootstraps user provided configurations.
    """

    def __init__(self, args):
        # type: (List[str]) -> None
        """Initializing the LocalDebugger Invoker by setting up WebSocketClient
         and SkillInvokerConfigurations based on passed cmd arguments.

        This class is the main method invoked by the debugger configuration.
        Bootstraps user provided configurations.

        :param args: List of arguments passed for local debugging.
        :type args: List[str]
        """
        parsed_args = argument_parser(args)
        self.web_socket_client = create_web_socket_client(parsed_args)

    def invoke(self):
        local_debugger = LocalDebugger(web_socket_client=self.web_socket_client)
        local_debugger.invoke()


if __name__ == "__main__":
    local_debug_invoker = LocalDebuggerInvoker(sys.argv[1:])
    local_debug_invoker.invoke()
