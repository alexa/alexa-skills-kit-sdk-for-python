Alexa Skills Kit SDK Sample - Color Picker
==========================================

A simple `AWS Lambda <http://aws.amazon.com/lambda>`__ function and the skill
interaction schema that demonstrates how to write a color picker skill for the
Amazon Echo using the Alexa Skill Kit Python SDK.

**NOTE**: This sample is subject to change during the beta period.

Concepts
--------

This sample shows how to create a Lambda function for handling Alexa
Skill requests that:

-  Demonstrates using custom slot types to handle a
   finite set of known values.
-  Use session attributes to store and pass session level attributes.
   In this example, favorite color is stored and passed on the skill
   session.
-  Use a catch-all exception handler, for catching all exceptions
   during skill invocation and return a meaningful response to the
   user. More on `exception handlers here <../../docs/REQUEST_PROCESSING.rst#exception-handlers>`__
-  Custom Request and Response Interceptors: This example shows two
   use cases of interceptors. More on the
   `request and response interceptors here <../../docs/REQUEST_PROCESSING.rst#request-and-response-interceptors>`__

    -  Log Alexa Request and Response objects using global interceptors.
    -  Add card to all responses, using the SSML text in ``outputSpeech``
       in response.

Setup
-----

To run this example skill you need to do two things. The first is to
deploy the example code in lambda, and the second is to configure the
Alexa skill to use Lambda.

Prerequisites
~~~~~~~~~~~~~

Please follow the
`prerequisites <../../docs/GETTING_STARTED.rst#prerequisites>`_ section and the
`adding ASK SDK <../../docs/GETTING_STARTED.rst#adding-the-ask-sdk-to-your-project>`_
section in
Getting Started documentation. For this sample skill, you only need
the ``ASK SDK Core`` package.

AWS Lambda Setup
~~~~~~~~~~~~~~~~

Refer to
`Hosting a Custom Skill as an AWS Lambda Function <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html>`__
reference for a walkthrough on creating a AWS Lambda function with the
correct role for your skill. When creating the function, select the
"Author from scratch" option, and select Python 2.7 or Python 3.6 runtime.

To prepare the skill for upload to AWS Lambda, create a zip file that
contains `color_picker.py <color_picker.py>`_, the SDK and it's dependencies.
Make sure to compress all files directly, **NOT** the project folder. You can
check the AWS Lambda docs to get more information on
`creating a deployment package <https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html>`_.

Once you’ve created your AWS Lambda function and configured "Alexa
Skills Kit" as a trigger, upload the ZIP file produced in the previous
step and set the handler to the fully qualified class name of your
handler function.  In this example, it would be ``color_picker.handler``.
Finally, copy the ARN for your AWS Lambda function
because you’ll need it when configuring your skill in the Amazon
Developer console.

Alexa Skill Setup
~~~~~~~~~~~~~~~~~

Now that the skill code has been uploaded to AWS Lambda we’re ready to
configure the skill with Alexa. First, navigate to the
`Alexa Skills Kit Developer Console <https://developer.amazon.com/alexa/console/ask>`__.
Click the "Create Skill" button in the upper right. Enter "ColorPicker"
as your skill name. On the next page, select "Custom" and click "Create
skill".

Now we’re ready to define the interaction model for the skill. Under
"Invocation" tab on the left side, define your Skill Invocation Name to
be ``color picker``.

Now it’s time to add an intent to the skill. Click the "Add" button
under the Intents section of the Interaction Model. Leave "Create custom
intent" selected, enter "WhatsMyColorIntent" for the intent name, and
create the intent. Now it’s time to add some sample utterances that will
be used to invoke the intent. For this example, we’ve provided the
following sample utterances, but feel free to add others.

::

   whats my color
   what is my color
   say my color
   tell me my color
   whats my favorite color
   what is my favorite color
   say my favorite color
   tell me my favorite color
   tell me what my favorite color is

Let’s add a Slot Type. You can find it below Built-In Intents.Click "Add
Slot Type" and under "Use an existing slot type from Alexa's built-in library",
search for "Color", and add "AMAZON.Color" slot type.

Let’s add another intent to the skill that has slots, called
"MyColorIsIntent" for intent name. Skip the sample utterances part for
now and create a new slot called "Color". Select Slot Type to be
"AMAZON.Color". Now add below sample utterances that uses this slot
"Color".

::

   my color is {Color}
   my favorite color is {Color}

Since **AMAZON.CancelIntent**, **AMAZON.HelpIntent**, and **AMAZON.StopIntent** are
built-in Alexa intents, sample utterances do not need to be provided as
they are automatically inherited.

The Developer Console alternately allows you to edit the entire skill
model in JSON format by selecting "JSON Editor" on the navigation bar.
For this sample, the
`interaction schema <speech_assets/interactionSchema.json>`_ can be used.

.. code:: json

   {
        "interactionModel": {
            "languageModel": {
                "invocationName": "my color picker",
                "intents": [
                    {
                        "name": "AMAZON.FallbackIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.CancelIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.HelpIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.StopIntent",
                        "samples": []
                    },
                    {
                        "name": "WhatsMyColorIntent",
                        "slots": [],
                        "samples": [
                            "tell me what is my favorite color",
                            "whats my favorite color",
                            "say my color",
                            "say my favorite color",
                            "tell me my favorite color",
                            "what is my favorite color",
                            "what is my color",
                            "whats my color"
                        ]
                    },
                    {
                        "name": "MyColorIsIntent",
                        "slots": [
                            {
                                "name": "Color",
                                "type": "AMAZON.Color"
                            }
                        ],
                        "samples": [
                            "My color is {Color}",
                            "my favorite color is {Color}"
                        ]
                    }
                ],
                "types": []
            }
        }
    }

Once you’re done editing the interaction model don’t forget to save and
build the model.

Let’s move on to the skill configuration section. Under "Endpoint"
select "AWS Lambda ARN" and paste in the ARN of the function you created
previously. The rest of the settings can be left at their default
values. Click "Save Endpoints" and proceed to the next section.

Under the AWS lambda function "Alexa Skills Kit" trigger, enable the "Skill Id
verification" and provide the Skill Id from the skill endpoint screen. Save
the lambda function.

Finally you’re ready to test the skill! In the "Test" tab of the
developer console you can simulate requests, in text and voice form, to
your skill. Use the invocation name along with one of the sample
utterances we just configured as a guide. You should also be able to go
to the `Echo webpage <http://echo.amazon.com/#skills>`__ and see your
skill listed under "Your Skills", where you can enable the skill on your
account for testing from an Alexa enabled device.

At this point, feel free to start experimenting with your Intent Schema
as well as the corresponding request handlers in your skill’s
implementation. Once you’re finished iterating, you can optionally
choose to move on to the process of getting your skill certified and
published so it can be used by Alexa users worldwide.

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

