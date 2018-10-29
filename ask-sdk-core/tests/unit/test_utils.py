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
from ask_sdk_model import (
    IntentRequest, RequestEnvelope, Intent, SessionEndedRequest)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.handler_input import HandlerInput


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

