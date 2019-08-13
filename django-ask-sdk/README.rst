======================================================
Django ASK SDK - Extending ASK SDK to work with Django
======================================================

**django-ask-sdk** is the extension package, that will let skill developers
use `ASK SDK <https://developer.amazon.com/docs/alexa-skills-kit-sdk-for-python/overview.html>`__
package in their Django application. It provides an easy way to register and
use `skills as custom webservices <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html>`__.

Quick Start
-----------

.. warning::

    These features are currently in beta. You can view the source
    code in the
    `Ask Python Sdk <https://github.com/alexa/alexa-skills-kit-sdk-for-python>`__
    repo on GitHub. The interface might change when the features are released as
    stable.

If you already have a skill built using the ASK SDK skill builders, then you
only need to do the following, to set this up in your django app (example_app):

example_app/my_skill.py
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.utils import is_request_type
    from ask_sdk_model import Response

    sb = SkillBuilder()

    class LaunchRequestHandler(AbstractRequestHandler):
        """Handler for skill launch."""
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_request_type("LaunchRequest")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            speech = "Hello"
            handler_input.response_builder.speak(speech)
            return handler_input.response_builder.response

    # Other skill components here ....

    # Register all handlers, interceptors etc.
    # For eg : sb.add_request_handler(LaunchRequestHandler())

    skill = sb.create()

example_app/urls.py
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from .my_skill import skill
    from django_ask_sdk.skill_adapter import SkillAdapter

    my_skill_view = SkillAdapter.as_view(
        skill=skill)

    urlpatterns = [
        path('/', my_skill_view, name='index'),
    ]

Are you planning to deploy your skill on AWS Lambda? Then, you don't even
need this package. The `ASK SDK` provides a `lambda_handler` that can be
directly used in your lambda console.

More code examples can be found `here <https://developer.amazon.com/docs/alexa-skills-kit-sdk-for-python/sample-skills.html>`__.

Features
--------

- Works as an extension on skills built using ASK SDK. No need to learn
  something new.
- Provides default request signature and request timestamp verification.
  These can be configured on app level by setting / unsetting default
  parameters on the view.
- Provides a way to register multiple skills on your app, at different
  endpoints.

Installation
------------

.. note::

    This package is compatible only with ``Python >= 3.6``, since it
    required ``Django >= 2.0`` which is only ``Python3`` compatible.

.. important::

    `cryptography` is a dependency for this package. If you have not
    already installed
    `cryptography <https://cryptography.io/en/latest/>`_, you might need to
    install additional prerequisites as detailed in the
    `cryptography installation guide <https://cryptography.io/en/latest/installation/>`_
    for your operating system.

Assuming that you have Python and ``virtualenv`` installed, you can
install the package and it's dependencies (``ask-sdk-webservice-support``)
from PyPi as follows:

.. code-block:: sh

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install django-ask-sdk


This package is **not** installed along-side `ask-sdk` standard distribution,
and has to be installed separately if you need support for skill
deployment as webservice, using Django.


SDK Usage and Getting Started
-----------------------------

Getting started guides, SDK Features, API references, samples etc. can
be found in the `technical documentation <https://developer.amazon.com/docs/alexa-skills-kit-sdk-for-python/overview.html>`_


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or
  quick feedback. Please search for the
  `existing issues <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`_
  before opening a new one. It would also be helpful if you follow the
  templates for issue and pull request creation. Please follow the
  `contributing guidelines <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`_!!
- Request and vote for `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!
