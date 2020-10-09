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
import sys
import typing

if typing.TYPE_CHECKING:
    from typing import Optional


def user_agent_info(sdk_version, custom_user_agent=None):
    # type: (str, Optional[str]) -> str
    """Return the user agent info along with the SDK and Python
    Version information.

    :param sdk_version: Version of the SDK being used.
    :type sdk_version: str
    :param custom_user_agent: Custom User Agent string provided by
        the developer.
    :type custom_user_agent: Optional[str]
    :return: User Agent Info string
    :rtype: str
    """
    python_version = ".".join(str(x) for x in sys.version_info[0:3])
    user_agent = "ask-python/{} Python/{}".format(
        sdk_version, python_version)
    if custom_user_agent is None:
        return user_agent
    else:
        return user_agent + " {}".format(custom_user_agent)


class UserAgentManager(object):
    """Static manager for environment level SDK user agent information.

    Higher level frameworks using the SDK, but not building up on skill builder,
    can use this static class and register their user agents.
    """
    _components = []
    _user_agent = ''

    @staticmethod
    def get_user_agent():
        # type: () -> str
        """Get user agent string containing all registered components.

        :return: User agent string with all registered components
        :rtype: str
        """
        return UserAgentManager._user_agent

    @staticmethod
    def register_component(component_name):
        # type: (str) -> None
        """Registers component to user agent string.

        The component will be appended to the existing user agent string.
        Duplicate components are ignored.

        :param component_name: Name of the component to be registered to
            the user agent string
        :type component_name: str
        :return: None
        """
        if component_name not in UserAgentManager._components:
            UserAgentManager._components.append(component_name)
            if UserAgentManager.get_user_agent() == '':
                UserAgentManager._user_agent = component_name
            else:
                UserAgentManager._user_agent = '{} {}'.format(
                    UserAgentManager.get_user_agent(), component_name)

    @staticmethod
    def clear():
        # type: () -> None
        """Clear components, reset user agent to empty.

        :return: None
        """
        UserAgentManager._components = []
        UserAgentManager._user_agent = ''
