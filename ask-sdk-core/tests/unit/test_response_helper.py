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

from ask_sdk_core.response_helper import (PLAIN_TEXT_TYPE, RICH_TEXT_TYPE,
                                          ResponseFactory,
                                          get_plain_text_content,
                                          get_rich_text_content,
                                          get_text_content)
from ask_sdk_model import directive
from ask_sdk_model.canfulfill import (CanFulfillIntent, CanFulfillIntentValues,
                                      CanFulfillSlot, CanFulfillSlotValues,
                                      CanUnderstandSlotValues)
from ask_sdk_model.interfaces.alexa.presentation.apla.render_document_directive import \
    RenderDocumentDirective
from ask_sdk_model.interfaces.display import PlainText, RichText, TextContent
from ask_sdk_model.interfaces.videoapp import (LaunchDirective, Metadata,
                                               VideoItem)
from ask_sdk_model.response import Response
from ask_sdk_model.ui import (Reprompt, SsmlOutputSpeech, output_speech,
                              reprompt, ssml_output_speech)
from ask_sdk_model.ui.play_behavior import PlayBehavior


class TestResponseFactory(unittest.TestCase):
    def setUp(self):
        self.response_factory = ResponseFactory()

    def test_speak(self):
        response_factory = self.response_factory.speak(speech=None)

        assert response_factory.response.output_speech == SsmlOutputSpeech(
            ssml="<speak></speak>"), (
            "The speak method of ResponseFactory fails to set output speech")

    def test_speak_with_play_behavior(self):
        test_play_behavior = PlayBehavior.ENQUEUE
        response_factory = self.response_factory.speak(
            speech=None, play_behavior=test_play_behavior)

        assert response_factory.response.output_speech == SsmlOutputSpeech(
            ssml="<speak></speak>", play_behavior=test_play_behavior), (
            "The speak method of ResponseFactory fails to set play behavior "
            "on output speech")

    def test_ask(self):
        response_factory = self.response_factory.ask(reprompt=None)

        assert response_factory.response.reprompt == Reprompt(
            output_speech=SsmlOutputSpeech(ssml="<speak></speak>")), (
            "The ask method of ResponseFactory fails to set reprompt")
        assert response_factory.response.should_end_session is False, (
            "The ask method of ResponseFactory fails to set the "
            "should_end_session to False")

    def test_ask_with_play_behavior(self):
        test_play_behavior = PlayBehavior.REPLACE_ALL
        response_factory = self.response_factory.ask(
            reprompt=None, play_behavior=test_play_behavior)

        assert response_factory.response.reprompt == Reprompt(
            output_speech=SsmlOutputSpeech(
                ssml="<speak></speak>",
                play_behavior=test_play_behavior)), (
            "The ask method of ResponseFactory fails to set play behavior "
            "on reprompt output speech")

    def test_ask_with_video_app_launch_directive(self):
        directive = LaunchDirective(video_item=VideoItem(
            source=None, metadata=Metadata(title=None, subtitle=None)))
        response_factory = self.response_factory.add_directive(
            directive).ask(reprompt=None)

        assert response_factory.response.should_end_session is None, (
            "The ask method of ResponseFactory fails to set the should_end "
            "session to None when video app directive"
            " presents")

    def test_ask_with_other_directive(self):
        response_factory = self.response_factory.add_directive(
            directive=None).ask(reprompt=None)

        assert response_factory.response.should_end_session is False, (
            "The ask method of ResponseFactory fails to set the "
            "should_end_session to False when other directives "
            "except video app directive presents")

    def test_set_card(self):
        response_factory = self.response_factory.set_card(card=None)

        assert response_factory.response.card is None, (
            "The set_card method of ResponseFactory fails to set card in "
            "response")

    def test_add_directives(self):
        response_factory = self.response_factory.add_directive(directive=None)

        assert len(response_factory.response.directives) == 1, (
            "The add_directive method of ResponseFactory fails to add "
            "directive")

    def test_add_two_directives(self):
        response_factory = self.response_factory.add_directive(
            directive=None).add_directive(directive=None)

        assert len(response_factory.response.directives) == 2, (
            "The add_directive method of ResponseFactory fails to add "
            "multiple directives")

    def test_add_reprompt_directive(self):
        response_factory = self.response_factory.add_directive_to_reprompt(directive=None)

        assert len(response_factory.response.reprompt.directives) == 1, (
            "The add_directive_to_reprompt method of ResponseFactory fails "
            "to add directive"
        )

    def test_response_with_reprompt_directive(self):
        directive = RenderDocumentDirective()
        expected_response = Response(
            output_speech=SsmlOutputSpeech(ssml="<speak>Hello World</speak>"),
            reprompt=Reprompt(directives=[directive]),
            should_end_session=False)

        response_factory = self.response_factory.set_should_end_session(True).add_directive_to_reprompt(
            directive=directive).speak('Hello World')
        assert response_factory.response == expected_response, (
            "The add_directive_to_reprompt method of ResponseFactory fails to add directive")

    def test_add_video_app_launch_directive(self):
        directive = LaunchDirective(video_item=VideoItem(
            source=None, metadata=Metadata(title=None, subtitle=None)))
        response_factory = self.response_factory.add_directive(
            directive).set_should_end_session(False)

        assert response_factory.response.directives[0] == directive, (
            "The add_directive method of ResponseFactory fails to add "
            "LaunchDirective")
        assert response_factory.response.should_end_session is None, (
            "The add_directive() method of ResponseFactory fails to "
            "remove should_end_session value")

    def test_set_should_end_session(self):
        response_factory = self.response_factory.set_should_end_session(False)

        assert response_factory.response.should_end_session is False, (
            "The set_should_end_session method of ResponseFactory fails to "
            "set should_end_session value")

    def test_trim_outputspeech(self):
        speech_output1 = "Hello World"
        speech_output2 = "  Hello World  "
        speech_output3 = "<speak>Hello World</speak>"
        speech_output4 = "<speak>  Hello World   </speak>"

        assert self.response_factory.speak(
            speech=speech_output1).response.output_speech.ssml == "<speak>Hello World</speak>", (
            "The trim_outputspeech method fails to trim the outputspeech")
        assert self.response_factory.speak(
            speech=speech_output2).response.output_speech.ssml == "<speak>Hello World</speak>", (
            "The trim_outputspeech method fails to trim the outputspeech")
        assert self.response_factory.speak(
            speech=speech_output3).response.output_speech.ssml == "<speak>Hello World</speak>", (
            "The trim_outputspeech method fails to trim the outputspeech")
        assert self.response_factory.speak(
            speech=speech_output4).response.output_speech.ssml == "<speak>Hello World</speak>", (
            "The trim_outputspeech method fails to trim the outputspeech")

    def test_set_can_fulfill_intent(self):
        intent = CanFulfillIntent(
            can_fulfill=CanFulfillIntentValues.MAYBE,
            slots={
                "testSlot": CanFulfillSlot(
                    can_understand=CanUnderstandSlotValues.YES,
                    can_fulfill=CanFulfillSlotValues.YES
                )
            }
        )
        response_factory = self.response_factory.set_can_fulfill_intent(
            can_fulfill_intent=intent)

        assert response_factory.response.can_fulfill_intent == intent, (
            "The set_can_fulfill_intent method of ResponseFactory fails to "
            "set can_fulfill_intent value")

    def test_set_api_response(self):
        test_api_response = {"arg1": "value1"}
        response_factory = self.response_factory.set_api_response(
            api_response=test_api_response)

        assert response_factory.response.api_response == test_api_response, (
            "The set_api_response method of ResponseFactory fails to "
            "set api_response value")


class TestTextHelper(unittest.TestCase):
    def test_build_primary_text_default(self):
        text_val = "test"

        plain_text = PlainText(text=text_val)
        text_content = TextContent(primary_text=plain_text)

        assert get_text_content(primary_text=text_val) == text_content, \
            "get_text_content helper returned wrong text content with " \
            "primary text and default type"

    def test_build_primary_text_rich(self):
        text_val = "test"

        rich_text = RichText(text=text_val)
        text_content = TextContent(primary_text=rich_text)

        assert get_text_content(
            primary_text=text_val, primary_text_type=RICH_TEXT_TYPE) == text_content, \
            "get_text_content helper returned wrong text content with " \
            "primary text and rich type"

    def test_build_secondary_text_default(self):
        text_val = "test"

        plain_text = PlainText(text=text_val)
        text_content = TextContent(secondary_text=plain_text)

        assert get_text_content(secondary_text=text_val) == text_content, \
            "get_text_content helper returned wrong text content with " \
            "secondary text and default type"

    def test_build_secondary_text_rich(self):
        text_val = "test"

        rich_text = RichText(text=text_val)
        text_content = TextContent(secondary_text=rich_text)

        assert get_text_content(
            secondary_text=text_val, secondary_text_type=RICH_TEXT_TYPE) == text_content, \
            "get_text_content helper returned wrong text content with " \
            "secondary text and rich type"

    def test_build_tertiary_text_default(self):
        text_val = "test"

        plain_text = PlainText(text=text_val)
        text_content = TextContent(tertiary_text=plain_text)

        assert get_text_content(tertiary_text=text_val) == text_content, \
            "get_text_content helper returned wrong text content with " \
            "tertiary text and default type"

    def test_build_tertiary_text_rich(self):
        text_val = "test"

        plain_text = RichText(text=text_val)
        text_content = TextContent(tertiary_text=plain_text)

        assert get_text_content(
            tertiary_text=text_val, tertiary_text_type=RICH_TEXT_TYPE) == text_content, \
            "get_text_content helper returned wrong text content with " \
            "tertiary text and rich type"

    def test_raise_value_error_with_invalid_text_type(self):
        text_val = "test"
        text_type = "InvalidType"

        with self.assertRaises(ValueError) as exc:
            get_text_content(primary_text=text_val, primary_text_type=text_type)

        assert "Invalid type provided" in str(exc.exception), \
            "get_text_content helper didn't raise ValueError when an " \
            "invalid type has been passed"


class TestPlainTextHelper(unittest.TestCase):
    def test_build_primary_text(self):
        text_val = "test"

        plain_text = PlainText(text=text_val)
        text_content = TextContent(primary_text=plain_text)

        assert get_plain_text_content(primary_text=text_val) == text_content, \
            "get_plain_text_content helper returned wrong text content " \
            "with primary text"


class TestRichTextHelper(unittest.TestCase):
    def test_build_primary_text(self):
        text_val = "test"

        rich_text = RichText(text=text_val)
        text_content = TextContent(primary_text=rich_text)

        assert get_rich_text_content(primary_text=text_val) == text_content, \
            "get_rich_text_content helper returned wrong text content " \
            "with primary text"
