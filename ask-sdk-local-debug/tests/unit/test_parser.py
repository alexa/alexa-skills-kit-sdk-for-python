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
import unittest

from ask_sdk_local_debug.exception import LocalDebugSdkException
from ask_sdk_local_debug.util.parser import argument_parser


class TestArgParse(unittest.TestCase):
    TEST_ACCESS_TOKEN = "test AccessToken"
    TEST_SKILL_FILE_PATH = "test/py/lambda.py"
    TEST_SKILL_HANDLER = "TestSkillHandler"
    TEST_SKILL_ID = "Skill ID 123234"

    def test_argument_parser_valid_args_with_access_token(self):
        test_args = list()
        test_args.extend(["--accessToken", self.TEST_ACCESS_TOKEN])
        test_args.extend(["--skillId", self.TEST_SKILL_ID])
        test_args.extend(["--skillFilePath", self.TEST_SKILL_FILE_PATH])
        test_args.extend(["--skillHandler", self.TEST_SKILL_HANDLER])

        args = argument_parser(test_args)
        self.assertEqual(args.access_token, self.TEST_ACCESS_TOKEN)
        self.assertEqual(args.skill_id, self.TEST_SKILL_ID)
        self.assertEqual(args.skill_file_path, self.TEST_SKILL_FILE_PATH)
        self.assertEqual(args.skill_handler, self.TEST_SKILL_HANDLER)

    def test_argument_parser_with_no_skill_id_and_no_access_token(self):
        test_args = list()
        test_args.extend(["--skillFilePath", self.TEST_SKILL_FILE_PATH])
        test_args.extend(["--skillHandler", self.TEST_SKILL_HANDLER])

        with self.assertRaises(LocalDebugSdkException) as exc:
            _ = argument_parser(test_args)

        self.assertEqual(
            "the following arguments are required: --accessToken, --skillId",
            str(exc.exception), (
                "argument_parser did not raise exception for null "
                "accessToken argument"))
