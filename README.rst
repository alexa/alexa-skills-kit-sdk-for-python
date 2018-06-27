===================
ASK SDK for Python
===================

The ASK SDK for Python makes it easier for you to build highly engaging skills,
by allowing you to spend more time on implementing features and less on writing
boiler-plate code.

To help you get started with the SDK we have included the following guides.
In the future, we plan to include more documentation and samples too.

Guides
------

`Setting Up The ASK SDK <docs/GETTING_STARTED.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This guide will show you how to include the SDK as a dependency in your
Python project.


`Developing Your First Skill <docs/DEVELOPING_YOUR_FIRST_SKILL.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Walks you through step-by-step instructions for building the Hello World
sample.


SDK Features
------------

`Request Processing <docs/REQUEST_PROCESSING.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Covers how to build request handlers, exception handlers, and request and
response interceptors.

`Skill Attributes <docs/ATTRIBUTES.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Covers how to use skill attributes to store and retrieve skill data.

`Response Building <docs/RESPONSE_BUILDING.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Covers how to use the ResponseBuilder to compose multiple elements like
text, cards, and audio into a single response.

`Alexa Service Clients <docs/SERVICE_CLIENTS.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Covers how to use service clients in your skill to access Alexa APIs.

`Skill Builders <docs/SKILL_BUILDERS.rst>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Covers how to configure and construct a skill instance.

Samples
-------

`Hello World Skill Sample <samples/HelloWorld>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This code sample will allow you to hear a response from Alexa when you
trigger it. It is a minimal sample to get you familiarized with the
Alexa Skills Kit and AWS Lambda.

`Color Picker Skill Sample <samples/ColorPicker>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a step-up in functionality from Hello World. It allows you to
capture input from your user and demonstrates the use of Slots. It also
demonstrates use of session attributes and request, response interceptors.

`High Low Game Skill Sample <samples/HighLowGame>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic high-low game skill. When the user guesses a number,
Alexa tells the user whether the number she has in mind is higher or lower.

`Device Address API Skill Sample <samples/GetDeviceAddress>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample skill that shows how to request and access the configured address in
the user’s device settings.


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for
  `existing issues <https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/issues>`_
  before opening a new one. It would also be helpful if you follow the
  templates for issue and pull request creation.
  Please follow the `contributing guidelines <CONTRIBUTING.rst>`_ for
  pull requests!!
- Request and vote for
  `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!


Additional Resources
--------------------

Community
~~~~~~~~~

-  `Amazon Developer Forums <https://forums.developer.amazon.com/spaces/165/index.html>`_ : Join the conversation!
-  `Hackster.io <https://www.hackster.io/amazon-alexa>`_ - See what others are building with Alexa.

Tutorials & Guides
~~~~~~~~~~~~~~~~~~

-  `Voice Design Guide <https://developer.amazon.com/designing-for-voice/>`_ -
   A great resource for learning conversational and voice user interface design.