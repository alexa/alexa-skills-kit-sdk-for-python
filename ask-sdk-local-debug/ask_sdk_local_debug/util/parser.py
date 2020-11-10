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
import argparse
import typing

from ask_sdk_local_debug.exception import LocalDebugSdkException

if typing.TYPE_CHECKING:
    from typing import List


class CustomArgumentParser(argparse.ArgumentParser):
    """CustomArgumentParser class to override the error function to throw
    a local debug Sdk Exception when invalid arguments are passed.
    """

    def __init__(self):
        # type: () -> None
        """Initialise CustomArgumentParser class and its parent class."""
        super(CustomArgumentParser, self).__init__()

    def error(self, message):
        # type: (str) -> None
        """Raise Local Debug Sdk Exception when invalid arguments are passed.

        :param message: Exception message raised.
        :type message: str
        :raises: :py:class:`ask_sdk_local_debug.exception.LocalDebugSdkException`
        """
        raise LocalDebugSdkException(message)


def argument_parser(args):
    # type: (List[str]) -> argparse.Namespace
    """The method processes CLI arguments used to invoke the local debug
    session.

    :param args: List of arguments used for local debugging.
    :type args: List[str]
    """
    parser = CustomArgumentParser()
    parser.add_argument("--accessToken", help='Authorization Token',
                        required=True, dest='access_token')
    parser.add_argument("--skillId", help='SkillId of the Skill',
                        required=True, dest='skill_id')
    parser.add_argument("--skillFilePath", help='Skill code file path',
                        required=True, dest='skill_file_path')
    parser.add_argument("--skillHandler", help='Skill Handler Name',
                        required=True, dest='skill_handler')
    parser.add_argument("--region", help='Region of the developer account',
                        required=False, dest='region', default="NA")

    return parser.parse_args(args)
