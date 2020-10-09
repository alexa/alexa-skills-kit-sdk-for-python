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
import unittest

from ask_sdk_runtime.utils import user_agent_info, UserAgentManager
from ask_sdk_runtime.__version__ import __version__


def test_user_agent_info_with_no_custom_user_agent():
    py_major_version = str(sys.version_info.major)
    py_minor_version = str(sys.version_info.minor)
    py_micro_version = str(sys.version_info.micro)

    expected_user_agent = "ask-python/{} Python/{}.{}.{}".format(
        __version__, py_major_version, py_minor_version, py_micro_version)
    assert user_agent_info(
        sdk_version=__version__,
        custom_user_agent=None) == expected_user_agent, (
        "Incorrect User Agent info for Null custom user agent")


def test_user_agent_info_with_custom_user_agent():
    py_major_version = str(sys.version_info.major)
    py_minor_version = str(sys.version_info.minor)
    py_micro_version = str(sys.version_info.micro)
    custom_user_agent = "test"

    expected_user_agent = "ask-python/{} Python/{}.{}.{} {}".format(
        __version__, py_major_version, py_minor_version,
        py_micro_version, custom_user_agent)
    assert user_agent_info(
        sdk_version=__version__,
        custom_user_agent=custom_user_agent) == expected_user_agent, (
        "Incorrect User Agent info for custom user agent")


class TestUserAgentManager(unittest.TestCase):
    def tearDown(self):
        UserAgentManager.clear()

    def test_user_agent_initialized(self):
        self.assertEqual(
            '', UserAgentManager.get_user_agent(),
            "UserAgent Manager didn't initialize user agent as empty string")

    def test_single_component_registered(self):
        test_component = "foo"
        UserAgentManager.register_component(test_component)
        self.assertEqual(
            test_component, UserAgentManager.get_user_agent(),
            "UserAgent Manager didn't register single component to "
            "user agent")

    def test_multi_component_registered(self):
        test_component_1 = "foo"
        test_component_2 = "bar"
        UserAgentManager.register_component(test_component_1)
        UserAgentManager.register_component(test_component_2)
        self.assertEqual(
            '{} {}'.format(test_component_1, test_component_2),
            UserAgentManager.get_user_agent(),
            "UserAgent Manager didn't register single component to "
            "user agent")

    def test_components_user_agent_cleared(self):
        UserAgentManager.register_component('foo')
        UserAgentManager.register_component('bar')
        UserAgentManager.clear()
        self.assertEqual(
            '', UserAgentManager.get_user_agent(),
            "UserAgent Manager didn't clear user agent")
