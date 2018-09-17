# -*- coding: utf-8 -*-
#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
#

# This is a skill for getting device address.
# The skill serves as a simple sample on how to use the
# service client factory and Alexa APIs through the SDK.

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_model.services import ServiceException

sb = CustomSkillBuilder(api_client=DefaultApiClient())

WELCOME = ("Welcome to the Sample Device Address API Skill!  "
           "You can ask for the device address by saying what is my "
           "address.  What do you want to ask?")
WHAT_DO_YOU_WANT = "What do you want to ask?"
NOTIFY_MISSING_PERMISSIONS = ("Please enable Location permissions in "
                              "the Amazon Alexa app.")
NO_ADDRESS = ("It looks like you don't have an address set. "
              "You can set your address from the companion app.")
ADDRESS_AVAILABLE = "Here is your full address: {}, {}, {}"
ERROR = "Uh Oh. Looks like something went wrong."
LOCATION_FAILURE = ("There was an error with the Device Address API. "
                    "Please try again.")
GOODBYE = "Bye! Thanks for using the Sample Device Address API Skill!"
UNHANDLED = "This skill doesn't support that. Please ask something else"
HELP = ("You can use this skill by asking something like: "
        "whats my address?")

permissions = ["read::alexa:device:all:address"]
# Location Consent permission to be shown on the card. More information
# can be checked at
# https://developer.amazon.com/docs/custom-skills/device-address-api.html#sample-response-with-permission-card


class LaunchRequestHandler(AbstractRequestHandler):
    # Handler for Skill Launch
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak(WELCOME).ask(WHAT_DO_YOU_WANT)
        return handler_input.response_builder.response


class GetAddressHandler(AbstractRequestHandler):
    # Handler for Getting Device Address or asking for location consent
    def can_handle(self, handler_input):
        return is_intent_name("GetAddressIntent")(handler_input)

    def handle(self, handler_input):
        req_envelope = handler_input.request_envelope
        response_builder = handler_input.response_builder
        service_client_fact = handler_input.service_client_factory

        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.user.permissions.consent_token):
            response_builder.speak(NOTIFY_MISSING_PERMISSIONS)
            response_builder.set_card(
                AskForPermissionsConsentCard(permissions=permissions))
            return response_builder.response

        try:
            device_id = req_envelope.context.system.device.device_id
            device_addr_client = service_client_fact.get_device_address_service()
            addr = device_addr_client.get_full_address(device_id)

            if addr.address_line1 is None and addr.state_or_region is None:
                response_builder.speak(NO_ADDRESS)
            else:
                response_builder.speak(ADDRESS_AVAILABLE.format(
                    addr.address_line1, addr.state_or_region, addr.postal_code))
            return response_builder.response
        except ServiceException:
            response_builder.speak(ERROR)
            return response_builder.response
        except Exception as e:
            raise e


class SessionEndedRequestHandler(AbstractRequestHandler):
    # Handler for Session End
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    # Handler for Help Intent
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak(HELP).ask(HELP)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    # Single handler for Cancel and Stop Intent
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        handler_input.response_builder.speak(GOODBYE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    # AMAZON.FallbackIntent is only available in en-US locale.
    # This handler will not be triggered except in that locale,
    # so it is safe to deploy on any locale
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak(UNHANDLED).ask(HELP)
        return handler_input.response_builder.response


class GetAddressExceptionHandler(AbstractExceptionHandler):
    # Custom Exception Handler for handling device address API call exceptions
    def can_handle(self, handler_input, exception):
        return isinstance(exception, ServiceException)

    def handle(self, handler_input, exception):
        if exception.status_code == 403:
            handler_input.response_builder.speak(
                NOTIFY_MISSING_PERMISSIONS).set_card(
                AskForPermissionsConsentCard(permissions=permissions))
        else:
            handler_input.response_builder.speak(
                LOCATION_FAILURE).ask(LOCATION_FAILURE)

        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    # Catch all exception handler, log exception and
    # respond with custom message
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print("Encountered following exception: {}".format(exception))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetAddressHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(GetAddressExceptionHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
