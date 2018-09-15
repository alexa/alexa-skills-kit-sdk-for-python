========================================
Source code for Hello World sample skill
========================================

As mentioned in the `Developing Your First Skill <DEVELOPING_YOUR_FIRST_SKILL.html>`_
section, we provide below the full source code for ``Hello World`` skill
using **classes** and **decorators**.

.. tabs::

    .. tab:: Classes

        .. code-block:: python

            # -*- coding: utf-8 -*-

            # This is a simple Hello World Alexa Skill, built using
            # the implementation of handler classes approach in skill builder.
            import logging

            from ask_sdk_core.skill_builder import SkillBuilder
            from ask_sdk_core.dispatch_components import AbstractRequestHandler
            from ask_sdk_core.dispatch_components import AbstractExceptionHandler
            from ask_sdk_core.utils import is_request_type, is_intent_name
            from ask_sdk_core.handler_input import HandlerInput

            from ask_sdk_model.ui import SimpleCard
            from ask_sdk_model import Response

            sb = SkillBuilder()

            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)


            class LaunchRequestHandler(AbstractRequestHandler):
                """Handler for Skill Launch."""
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    return is_request_type("LaunchRequest")(handler_input)

                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

                    handler_input.response_builder.speak(speech_text).set_card(
                        SimpleCard("Hello World", speech_text)).set_should_end_session(
                        False)
                    return handler_input.response_builder.response


            class HelloWorldIntentHandler(AbstractRequestHandler):
                """Handler for Hello World Intent."""
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    return is_intent_name("HelloWorldIntent")(handler_input)

                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    speech_text = "Hello Python World from Classes!"

                    handler_input.response_builder.speak(speech_text).set_card(
                        SimpleCard("Hello World", speech_text)).set_should_end_session(
                        True)
                    return handler_input.response_builder.response


            class HelpIntentHandler(AbstractRequestHandler):
                """Handler for Help Intent."""
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    return is_intent_name("AMAZON.HelpIntent")(handler_input)

                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    speech_text = "You can say hello to me!"

                    handler_input.response_builder.speak(speech_text).ask(
                        speech_text).set_card(SimpleCard(
                            "Hello World", speech_text))
                    return handler_input.response_builder.response


            class CancelOrStopIntentHandler(AbstractRequestHandler):
                """Single handler for Cancel and Stop Intent."""
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                            is_intent_name("AMAZON.StopIntent")(handler_input))

                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    speech_text = "Goodbye!"

                    handler_input.response_builder.speak(speech_text).set_card(
                        SimpleCard("Hello World", speech_text))
                    return handler_input.response_builder.response


            class FallbackIntentHandler(AbstractRequestHandler):
                """AMAZON.FallbackIntent is only available in en-US locale.
                This handler will not be triggered except in that locale,
                so it is safe to deploy on any locale.
                """
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    return is_intent_name("AMAZON.FallbackIntent")(handler_input)

                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    speech_text = (
                        "The Hello World skill can't help you with that.  "
                        "You can say hello!!")
                    reprompt = "You can say hello!!"
                    handler_input.response_builder.speak(speech_text).ask(reprompt)
                    return handler_input.response_builder.response


            class SessionEndedRequestHandler(AbstractRequestHandler):
                """Handler for Session End."""
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    return is_request_type("SessionEndedRequest")(handler_input)

                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    return handler_input.response_builder.response


            class CatchAllExceptionHandler(AbstractExceptionHandler):
                """Catch all exception handler, log exception and
                respond with custom message.
                """
                def can_handle(self, handler_input, exception):
                    # type: (HandlerInput, Exception) -> bool
                    return True

                def handle(self, handler_input, exception):
                    # type: (HandlerInput, Exception) -> Response
                    logger.error(exception, exc_info=True)

                    speech = "Sorry, there was some problem. Please try again!!"
                    handler_input.response_builder.speak(speech).ask(speech)

                    return handler_input.response_builder.response


            sb.add_request_handler(LaunchRequestHandler())
            sb.add_request_handler(HelloWorldIntentHandler())
            sb.add_request_handler(HelpIntentHandler())
            sb.add_request_handler(CancelOrStopIntentHandler())
            sb.add_request_handler(FallbackIntentHandler())
            sb.add_request_handler(SessionEndedRequestHandler())

            sb.add_exception_handler(CatchAllExceptionHandler())

            handler = sb.lambda_handler()

    .. tab:: Decorators

        .. code-block:: python

            # -*- coding: utf-8 -*-

            # This is a simple Hello World Alexa Skill, built using
            # the decorators approach in skill builder.
            import logging

            from ask_sdk_core.skill_builder import SkillBuilder
            from ask_sdk_core.utils import is_request_type, is_intent_name
            from ask_sdk_core.handler_input import HandlerInput

            from ask_sdk_model.ui import SimpleCard
            from ask_sdk_model import Response

            sb = SkillBuilder()

            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)


            @sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
            def launch_request_handler(handler_input):
                """Handler for Skill Launch."""
                # type: (HandlerInput) -> Response
                speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

                return handler_input.response_builder.speak(speech_text).set_card(
                    SimpleCard("Hello World", speech_text)).set_should_end_session(
                    False).response


            @sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
            def hello_world_intent_handler(handler_input):
                """Handler for Hello World Intent."""
                # type: (HandlerInput) -> Response
                speech_text = "Hello Python World from Decorators!"

                return handler_input.response_builder.speak(speech_text).set_card(
                    SimpleCard("Hello World", speech_text)).set_should_end_session(
                    True).response


            @sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
            def help_intent_handler(handler_input):
                """Handler for Help Intent."""
                # type: (HandlerInput) -> Response
                speech_text = "You can say hello to me!"

                return handler_input.response_builder.speak(speech_text).ask(
                    speech_text).set_card(SimpleCard(
                        "Hello World", speech_text)).response


            @sb.request_handler(
                can_handle_func=lambda handler_input:
                    is_intent_name("AMAZON.CancelIntent")(handler_input) or
                    is_intent_name("AMAZON.StopIntent")(handler_input))
            def cancel_and_stop_intent_handler(handler_input):
                """Single handler for Cancel and Stop Intent."""
                # type: (HandlerInput) -> Response
                speech_text = "Goodbye!"

                return handler_input.response_builder.speak(speech_text).set_card(
                    SimpleCard("Hello World", speech_text)).response


            @sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
            def fallback_handler(handler_input):
                """AMAZON.FallbackIntent is only available in en-US locale.
                This handler will not be triggered except in that locale,
                so it is safe to deploy on any locale.
                """
                # type: (HandlerInput) -> Response
                speech = (
                    "The Hello World skill can't help you with that.  "
                    "You can say hello!!")
                reprompt = "You can say hello!!"
                handler_input.response_builder.speak(speech).ask(reprompt)
                return handler_input.response_builder.response


            @sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
            def session_ended_request_handler(handler_input):
                """Handler for Session End."""
                # type: (HandlerInput) -> Response
                return handler_input.response_builder.response


            @sb.exception_handler(can_handle_func=lambda i, e: True)
            def all_exception_handler(handler_input, exception):
                """Catch all exception handler, log exception and
                respond with custom message.
                """
                # type: (HandlerInput, Exception) -> Response
                logger.error(exception, exc_info=True)

                speech = "Sorry, there was some problem. Please try again!!"
                handler_input.response_builder.speak(speech).ask(speech)

                return handler_input.response_builder.response


            handler = sb.lambda_handler()
