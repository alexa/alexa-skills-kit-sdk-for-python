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
import unittest
import random

from ask_sdk_model import (
    IntentRequest, RequestEnvelope, Intent, SessionEndedRequest, Context,
    LaunchRequest, DialogState, Slot, Session, User, Device,
    SupportedInterfaces)
from ask_sdk_model.canfulfill import CanFulfillIntentRequest
from ask_sdk_model.interfaces.viewport import ViewportState, Shape
from ask_sdk_model.interfaces.system import SystemState
from ask_sdk_model.interfaces.display import DisplayInterface
from ask_sdk_core.utils import (
    is_canfulfill_intent_name, is_intent_name, is_request_type, viewport,
    get_slot, get_slot_value, get_account_linking_access_token,
    get_api_access_token, get_device_id, get_dialog_state, get_intent_name,
    get_locale, get_request_type, is_new_session, get_supported_interfaces)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.exceptions import AskSdkException


def test_is_canfulfill_intent_name_match():
    test_canfulfill_intent_name = "TestIntent"
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=CanFulfillIntentRequest(
            intent=Intent(name=test_canfulfill_intent_name))))

    canfulfill_intent_name_wrapper = is_canfulfill_intent_name(test_canfulfill_intent_name)
    assert canfulfill_intent_name_wrapper(
        test_handler_input), "is_canfulfill_intent_name matcher didn't match with the " \
                             "correct intent name"


def test_is_canfulfill_intent_name_not_match():
    test_canfulfill_intent_name = "TestIntent"
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=CanFulfillIntentRequest(
            intent=Intent(name=test_canfulfill_intent_name))))

    canfulfill_intent_name_wrapper = is_canfulfill_intent_name("TestIntent1")
    assert not canfulfill_intent_name_wrapper(
        test_handler_input), "is_canfulfill_intent_name matcher matched with the " \
                             "incorrect intent name"


def test_is_canfulfill_intent_not_match_intent():
    test_canfulfill_intent_name = "TestIntent"
    test_canfulfill_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=CanFulfillIntentRequest(
            intent=Intent(name=test_canfulfill_intent_name))))

    intent_name_wrapper = is_intent_name(test_canfulfill_intent_name)
    assert not intent_name_wrapper(
        test_canfulfill_handler_input), "is_intent_name matcher matched with the " \
                                        "incorrect request type"


def test_is_intent_not_match_canfulfill_intent():
    test_intent_name = "TestIntent"
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=IntentRequest(
            intent=Intent(name=test_intent_name))))

    canfulfill_intent_name_wrapper = is_canfulfill_intent_name(test_intent_name)
    assert not canfulfill_intent_name_wrapper(
        test_handler_input), "is_canfulfill_intent_name matcher matched with the " \
                             "incorrect request type"


def test_is_intent_name_match():
    test_intent_name = "TestIntent"
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=IntentRequest(
            intent=Intent(name=test_intent_name))))

    intent_name_wrapper = is_intent_name(test_intent_name)
    assert intent_name_wrapper(
        test_handler_input), "is_intent_name matcher didn't match with the " \
                             "correct intent name"


def test_is_intent_name_not_match():
    test_intent_name = "TestIntent"
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=IntentRequest(
            intent=Intent(name=test_intent_name))))

    intent_name_wrapper = is_intent_name("TestIntent1")
    assert not intent_name_wrapper(
        test_handler_input), "is_intent_name matcher matched with the " \
                             "incorrect intent name"


def test_is_request_type_match():
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=IntentRequest()))

    request_type_wrapper = is_request_type("IntentRequest")
    assert request_type_wrapper(test_handler_input), (
        "is_request_type matcher didn't match with the correct request type")


def test_is_request_type_not_match():
    test_handler_input = HandlerInput(
        request_envelope=RequestEnvelope(request=SessionEndedRequest()))

    intent_name_wrapper = is_request_type("IntentRequest")
    assert not intent_name_wrapper(test_handler_input), (
        "is_request_type matcher matched with the incorrect request type")


class TestViewportOrientation(unittest.TestCase):
    def test_portrait_orientation(self):
        width = 0
        height = 1
        assert (viewport.get_orientation(width=width, height=height)
                == viewport.Orientation.PORTRAIT), (
            "Invalid viewport orientation resolved when width < height")

    def test_landscape_orientation(self):
        width = 1
        height = 0
        assert (viewport.get_orientation(width=width, height=height)
                == viewport.Orientation.LANDSCAPE), (
            "Invalid viewport orientation resolved when width > height")

    def test_equal_orientation(self):
        width = 0
        height = 0
        assert (viewport.get_orientation(width=width, height=height)
                == viewport.Orientation.EQUAL), (
            "Invalid viewport orientation resolved when width == height")


class TestViewportSize(unittest.TestCase):
    def test_xsmall_size(self):
        size = random.choice(range(0, 600))
        assert (viewport.get_size(size=size)
                == viewport.Size.XSMALL), (
            "Invalid viewport size resolved when size = {}".format(size))

    def test_small_size(self):
        size = random.choice(range(600, 960))
        assert (viewport.get_size(size=size)
                == viewport.Size.SMALL), (
            "Invalid viewport size resolved when size = {}".format(size))

    def test_medium_size(self):
        size = random.choice(range(960, 1280))
        assert (viewport.get_size(size=size)
                == viewport.Size.MEDIUM), (
            "Invalid viewport size resolved when size = {}".format(size))

    def test_large_size(self):
        size = random.choice(range(1280, 1920))
        assert (viewport.get_size(size=size)
                == viewport.Size.LARGE), (
            "Invalid viewport size resolved when size = {}".format(size))

    def test_xlarge_size(self):
        size = 1920
        assert (viewport.get_size(size=size)
                == viewport.Size.XLARGE), (
            "Invalid viewport size resolved when size = {}".format(size))

    def test_unknown_size(self):
        size = -1
        with self.assertRaises(AskSdkException) as exc_info:
            viewport.get_size(size=size)

        assert "Unknown size group value: -1" in str(exc_info.exception), (
            "Viewport size resolver didn't raise exception on invalid size"
        )


class TestViewportDpiGroup(unittest.TestCase):
    def test_xlow_dpi_group(self):
        dpi = random.choice(range(0, 121))
        assert (viewport.get_dpi_group(dpi=dpi)
                == viewport.Density.XLOW), (
            "Invalid viewport dpi_group resolved when dpi = {}".format(dpi))

    def test_low_dpi_group(self):
        dpi = random.choice(range(121, 161))
        assert (viewport.get_dpi_group(dpi=dpi)
                == viewport.Density.LOW), (
            "Invalid viewport dpi_group resolved when dpi = {}".format(dpi))

    def test_medium_dpi_group(self):
        dpi = random.choice(range(161, 241))
        assert (viewport.get_dpi_group(dpi=dpi)
                == viewport.Density.MEDIUM), (
            "Invalid viewport dpi_group resolved when dpi = {}".format(dpi))

    def test_high_dpi_group(self):
        dpi = random.choice(range(241, 321))
        assert (viewport.get_dpi_group(dpi=dpi)
                == viewport.Density.HIGH), (
            "Invalid viewport dpi_group resolved when dpi = {}".format(dpi))

    def test_xhigh_dpi_group(self):
        dpi = random.choice(range(321, 481))
        assert (viewport.get_dpi_group(dpi=dpi)
                == viewport.Density.XHIGH), (
            "Invalid viewport dpi_group resolved when dpi = {}".format(dpi))

    def test_xxhigh_dpi_group(self):
        dpi = 481
        assert (viewport.get_dpi_group(dpi=dpi)
                == viewport.Density.XXHIGH), (
            "Invalid viewport dpi_group resolved when dpi = {}".format(dpi))

    def test_unknown_dpi_group(self):
        dpi = -1
        with self.assertRaises(AskSdkException) as exc_info:
            viewport.get_dpi_group(dpi=dpi)

        assert "Unknown dpi group value: -1" in str(exc_info.exception), (
            "Viewport dpi group resolver didn't raise exception on invalid dpi"
        )


class TestViewportProfile(unittest.TestCase):
    def test_viewport_map_to_hub_round_small(self):
        viewport_state = ViewportState(
            shape=Shape.ROUND,
            dpi=float(160),
            current_pixel_width=float(300),
            current_pixel_height=float(300))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.HUB_ROUND_SMALL), (
            "Viewport profile couldn't resolve HUB_ROUND_SMALL")

    def test_viewport_map_to_hub_landscape_medium(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(160),
            current_pixel_width=float(960),
            current_pixel_height=float(600))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM), (
            "Viewport profile couldn't resolve HUB_LANDSCAPE_MEDIUM")

    def test_viewport_map_to_hub_landscape_large(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(160),
            current_pixel_width=float(1280),
            current_pixel_height=float(960))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.HUB_LANDSCAPE_LARGE), (
            "Viewport profile couldn't resolve HUB_LANDSCAPE_LARGE")

    def test_viewport_map_to_mobile_landscape_small(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(240),
            current_pixel_width=float(600),
            current_pixel_height=float(300))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL), (
            "Viewport profile couldn't resolve MOBILE_LANDSCAPE_SMALL")

    def test_viewport_map_to_mobile_portrait_small(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(240),
            current_pixel_width=float(300),
            current_pixel_height=float(600))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.MOBILE_PORTRAIT_SMALL), (
            "Viewport profile couldn't resolve MOBILE_PORTRAIT_SMALL")

    def test_viewport_map_to_mobile_landscape_medium(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(240),
            current_pixel_width=float(960),
            current_pixel_height=float(600))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.MOBILE_LANDSCAPE_MEDIUM), (
            "Viewport profile couldn't resolve MOBILE_LANDSCAPE_MEDIUM")

    def test_viewport_map_to_mobile_portrait_medium(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(240),
            current_pixel_width=float(600),
            current_pixel_height=float(960))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.MOBILE_PORTRAIT_MEDIUM), (
            "Viewport profile couldn't resolve MOBILE_PORTRAIT_MEDIUM")

    def test_viewport_map_to_tv_landscape_xlarge(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(320),
            current_pixel_width=float(1920),
            current_pixel_height=float(960))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.TV_LANDSCAPE_XLARGE), (
            "Viewport profile couldn't resolve TV_LANDSCAPE_XLARGE")

    def test_viewport_map_to_tv_portrait_medium(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(320),
            current_pixel_width=float(300),
            current_pixel_height=float(1920))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.TV_PORTRAIT_MEDIUM), (
            "Viewport profile couldn't resolve TV_PORTRAIT_MEDIUM")

    def test_viewport_map_to_tv_landscape_medium(self):
        viewport_state = ViewportState(
            shape=Shape.RECTANGLE,
            dpi=float(320),
            current_pixel_width=float(960),
            current_pixel_height=float(600))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.TV_LANDSCAPE_MEDIUM), (
            "Viewport profile couldn't resolve TV_LANDSCAPE_MEDIUM")

    def test_viewport_map_to_unknown(self):
        viewport_state = ViewportState(
            shape=Shape.ROUND,
            dpi=float(240),
            current_pixel_width=float(600),
            current_pixel_height=float(600))
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.UNKNOWN_VIEWPORT_PROFILE), (
            "Viewport profile couldn't resolve UNKNOWN_VIEWPORT_PROFILE")

    def test_viewport_map_to_unknown_for_no_viewport(self):
        viewport_state = None
        test_request_env = RequestEnvelope(
            context=Context(
                viewport=viewport_state))

        assert (viewport.get_viewport_profile(test_request_env)
                is viewport.ViewportProfile.UNKNOWN_VIEWPORT_PROFILE), (
            "Viewport profile couldn't resolve UNKNOWN_VIEWPORT_PROFILE")


class TestRequestUtils(unittest.TestCase):

    def setUp(self):
        self.test_locale = "foo_locale"
        self.test_request_type = "LaunchRequest"
        self.test_dialog_state = DialogState.COMPLETED
        self.test_intent_name = "foo_intent"
        self.test_slot_name = "foo_slot"
        self.test_slot_value = "foo_slot_value"
        self.test_slot = Slot(
            name=self.test_slot_name, value=self.test_slot_value)
        self.test_api_access_token = "foo_api_access_token"
        self.test_access_token = "foo_account_linking_access_token"
        self.test_device_id = "foo_device_id"
        self.test_supported_interfaces = SupportedInterfaces(
            display=DisplayInterface(
                template_version="test_template", markup_version="test_markup")
        )
        self.test_new_session = False

        self.test_launch_request = LaunchRequest(locale=self.test_locale)
        self.test_intent_request = IntentRequest(
            dialog_state=self.test_dialog_state,
            intent=Intent(
                name=self.test_intent_name,
                slots={
                    self.test_slot_name: Slot(
                        name=self.test_slot_name,
                        value=self.test_slot_value)
                }))
        self.test_request_envelope = RequestEnvelope(
            session=Session(new=self.test_new_session),
            context=Context(
                system=SystemState(
                    user=User(access_token=self.test_access_token),
                    api_access_token=self.test_api_access_token,
                    device=Device(
                        device_id=self.test_device_id,
                        supported_interfaces=self.test_supported_interfaces))))

    def _create_handler_input(self, request):
        self.test_request_envelope.request = request
        return HandlerInput(request_envelope=self.test_request_envelope)

    def test_get_locale(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            get_locale(handler_input=test_input), self.test_locale,
            "get_locale method returned incorrect locale for input request")

    def test_get_request_type(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            get_request_type(handler_input=test_input), self.test_request_type,
            "get_request_type method returned incorrect request type for "
            "input request")

    def test_get_intent_name_throws_exception_for_non_intent_request(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        with self.assertRaises(
                TypeError,
                msg="get_intent_name method didn't throw TypeError when an "
                    "invalid request type is passed"):
            get_intent_name(handler_input=test_input)

    def test_get_intent_name(self):
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        self.assertEqual(
            get_intent_name(handler_input=test_input), self.test_intent_name,
            "get_intent_name method returned incorrect intent name for "
            "input request")

    def test_get_account_linking_access_token(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            get_account_linking_access_token(handler_input=test_input),
            self.test_access_token,
            "get_account_linking_access_token method returned incorrect "
            "access token from input request")

    def test_get_api_access_token(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            get_api_access_token(handler_input=test_input),
            self.test_api_access_token,
            "get_api_access_token method returned incorrect "
            "api access token from input request")

    def test_get_device_id(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            get_device_id(handler_input=test_input),
            self.test_device_id,
            "get_device_id method returned incorrect "
            "device id from input request")

    def test_get_dialog_state_throws_exception_for_non_intent_request(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        with self.assertRaises(
                TypeError,
                msg="get_dialog_state method didn't throw TypeError when an "
                    "invalid request type is passed"):
            get_dialog_state(handler_input=test_input)

    def test_get_dialog_state(self):
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        self.assertEqual(
            get_dialog_state(handler_input=test_input),
            self.test_dialog_state,
            "get_dialog_state method returned incorrect "
            "dialog state from input request")

    def test_get_slot_throws_exception_for_non_intent_request(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        with self.assertRaises(
                TypeError,
                msg="get_slot method didn't throw TypeError when an "
                    "invalid request type is passed"):
            get_slot(handler_input=test_input, slot_name=self.test_slot_name)

    def test_get_slot_returns_none_for_no_slots(self):
        self.test_intent_request.intent.slots = None
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        self.assertEqual(
            get_slot(handler_input=test_input, slot_name="some_slot"),
            None,
            "get_slot method didn't return None from input request "
            "when intent request has no slots")

    def test_get_slot_returns_none_for_non_existent_slot(self):
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        self.assertEqual(
            get_slot(handler_input=test_input, slot_name="some_slot"),
            None,
            "get_slot method didn't return None from input request "
            "when a non-existent slot name is passed")

    def test_get_slot(self):
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        self.assertEqual(
            get_slot(handler_input=test_input, slot_name=self.test_slot_name),
            self.test_slot,
            "get_slot method returned incorrect slot from input request "
            "when a valid slot name is passed")

    def test_get_slot_value_throws_exception_for_non_intent_request(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        with self.assertRaises(
                TypeError,
                msg="get_slot_value method didn't throw TypeError when an "
                    "invalid request type is passed"):
            get_slot_value(
                handler_input=test_input, slot_name=self.test_slot_name)

    def test_get_slot_value_throws_exception_for_non_existent_slot(self):
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        with self.assertRaises(
                ValueError,
                msg="get_slot_value method didn't throw ValueError when an "
                    "invalid slot name is passed"):
            get_slot_value(handler_input=test_input, slot_name="some_slot")

    def test_get_slot_value(self):
        test_input = self._create_handler_input(
            request=self.test_intent_request)

        self.assertEqual(
            get_slot_value(
                handler_input=test_input, slot_name=self.test_slot_name),
            self.test_slot_value,
            "get_slot_value method returned incorrect slot value from "
            "input request when a valid slot name is passed")

    def test_get_supported_interfaces(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            get_supported_interfaces(handler_input=test_input),
            self.test_supported_interfaces,
            "get_supported_interfaces method returned incorrect "
            "supported interfaces from input request")

    def test_is_new_session_throws_exception_if_session_not_exists(self):
        test_input = HandlerInput(request_envelope=RequestEnvelope())

        with self.assertRaises(
                TypeError,
                msg="is_new_session method didn't throw TypeError when an "
                    "input request without session is passed"):
            is_new_session(handler_input=test_input)

    def test_is_new_session(self):
        test_input = self._create_handler_input(
            request=self.test_launch_request)

        self.assertEqual(
            is_new_session(handler_input=test_input),
            self.test_new_session,
            "is_new_session method returned incorrect session information "
            "from input request when a session exists")
