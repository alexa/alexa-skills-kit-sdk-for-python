====================================================
ASK SDK Jinja Renderer
====================================================
ask-sdk-jinja-renderer is an SDK package for supporting template responses for skill developers, when built using
ASK Python SDK. It provides jinja framework as a template renderer to render the response loaded from the
template and inject the data passed and finally deserialize to custom response format.

Quick Start
-----------
If you already have a skill built using the ASK SDK builders, then you only need to do the following,
to start using template resolvers to generate responses.

- Import FileSystemTemplateLoader from ask_sdk_core and JinjaTemplateRenderer from ask_sdk_jinja_renderer packages.
- Register the Loaders with appropriate parameters and also a Renderer into skill builder using add_loaders and
  add_renderer methods.
- Create a template file as shown below and provide the path of the directory and its encoding scheme as parameters while
  initializing the loader.

example_app/my_skill.py
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.utils import is_request_type
    from ask_sdk_core.view_resolvers import FileSystemTemplateLoader
    from ask_sdk_jinja_renderer import JinjaTemplateRenderer
    from ask_sdk_model import Response

    sb = SkillBuilder()

    class LaunchRequestHandler(AbstractRequestHandler):
        """Handler for skill launch."""
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_request_type("LaunchRequest")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            speech_text = "Hello!!"

            template_name = "responses"

            data_map = {
                'speech_text': speech_text,
                'card': {
                    'type': 'Simple',
                    'title': 'Jinja2 Template',
                    'content': speech_text
                },
                'should_end_session': 'false'
            }

            return handler_input.generate_template_response(template_name, data_map, file_ext='jinja')

    # Other skill components here ....

    # Register all handlers, loaders, renderers, interceptors etc.
    sb.add_request_handler(LaunchRequestHandler())
    # Add default file system loader on skill builder
    sb.add_loader(FileSystemTemplateLoader(dir_path="templates", encoding='utf-8'))
    # Add default jinja renderer on skill builder
    sb.add_renderer(JinjaTemplateRenderer())


    skill = sb.create()


example_app/templates/responses.jinja
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: json

    {
        "outputSpeech": {
            "type": "SSML",
            "ssml": "<speak>{{ speech_text }}</speak>"
        },
        "card": {
            "type": "{{ card.type }}",
            "title": "{{ card.title}}",
            "content": "{{ card.content }}"
        },
        "shouldEndSession": "{{ should_end_session }}"
    }



Installation
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, you can
install the package from PyPi as follows:

.. code-block:: sh

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install ask-sdk-jinja-renderer


Usage and Getting Started
-------------------------

Getting started guides, SDK Features, API references, samples etc. can
be found at `Read The Docs <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/>`_


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for the `existing issues <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`_ before opening a new one. It would also be helpful
  if you follow the templates for issue and pull request creation. Please follow the `contributing guidelines <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`_!!
- Request and vote for `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!
