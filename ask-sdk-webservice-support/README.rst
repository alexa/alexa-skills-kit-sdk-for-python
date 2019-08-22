===================================================================================
ASK SDK Webservice Support - Base components for Python ASK SDK Skill as WebService
===================================================================================

**ask-sdk-webservice-support** is the base SDK package for providing
support to deploy skill as webservice, when built using ASK Python SDK.
It provides the base verification components and the dispatch logic for
skills deployed as a custom webservice rather than on AWS Lambda.
It provides an easy way to register and use
`skills as custom webservices <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html>`__.

If you plan to use `Flask` for your webservice development, you can
install the `flask-ask-sdk` package. If you are using `Django` for your
webservice development, you can install the `django-ask-sdk` package.


Quick Start
-----------

Installation
~~~~~~~~~~~~~

.. important::

    `cryptography` is a dependency for this package. If you have not
    already installed
    `cryptography <https://cryptography.io/en/latest/>`_, you might need to
    install additional prerequisites as detailed in the
    `cryptography installation guide <https://cryptography.io/en/latest/installation/>`_
    for your operating system.

Assuming that you have Python and ``virtualenv`` installed, you can
install the package from PyPi as follows:

.. code-block:: sh

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install ask-sdk-webservice-support

This package is not installed along-side `ask-sdk` standard distribution,
and has to be installed separately if you need support for skill
deployment as webservice.


Usage and Getting Started
-------------------------

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
