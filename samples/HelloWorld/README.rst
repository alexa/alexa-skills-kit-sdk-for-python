Alexa Skills Kit SDK Sample - Hello World
=========================================

A simple `AWS Lambda <http://aws.amazon.com/lambda>`__ function that
demonstrates how to write a Hello World skill for the Amazon Echo using
the Alexa SDK.

Concepts
--------

This simple sample has no external dependencies or session management,
and shows the most basic example of how to create a Lambda function for
handling Alexa Skill requests.

Setup
-----

To run this example skill you need to do two things. The first is to
deploy the example code in lambda, and the second is to configure the
Alexa skill to use Lambda.

This sample skills shows two ways of developing skills:

- Implementing ``AbstractRequestHandler`` class and registering the
  handler classes explicitly in the skill builder object. The code for this
  implementation is under `skill_using_classes <skill_using_classes>`_ folder.
- Using the skill builder's ``request_handler`` decorator, and
  decorating custom functions that responds to intents. The code for this
  implementation is under `skill_using_decorators <skill_using_decorators>`_
  folder.

For detailed instructions, please refer to
`Developing Your First Skill <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html>`__

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

Documentation
~~~~~~~~~~~~~

-  `Official Alexa Skills Kit Python SDK Docs <../../README.rst>`_
-  `Official Alexa Skills Kit Docs <https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html>`_

