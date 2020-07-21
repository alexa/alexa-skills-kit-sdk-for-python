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


class ClientConfiguration(object):
    """Client configuration class for local debugging.

    Builds instance of client configuration which gets the skill id for
    the skill being debugged, LWA authentication configuration module and
    it's entry point to invoke the skill.
    """
    def __init__(self, access_token, skill_id, skill_file_path, skill_handler):
        # type: (str, str, str, str) -> None
        """Builds instance of client configuration which gets the skill id for
        the skill being debugged, LWA access token, module and
        it's entry point to invoke the skill.

        :param access_token: LWA Access token required to make
            local debug web socket connection.
        :type access_token: str
        :param skill_id: SkillId of a skill
        :type skill_id: str
        :param skill_file_path: Entry file path of skill code for local debug.
        :type skill_file_path: str
        :param skill_handler: Handler function to invoke for debug session.
        :type skill_handler: str
        """
        self.access_token = access_token
        self.skill_id = skill_id
        self.skill_file_path = skill_file_path
        self.skill_handler = skill_handler
