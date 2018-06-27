Alexa Skills Kit SDK Sample - High Low Game
===========================================

This Alexa sample skill is a template for a basic high-low game skill.
Guess a number, and Alexa will tell you whether the number she has in mind
is higher or lower.

**NOTE**: This sample is subject to change during the beta period.

Concepts
--------

This sample shows how to create a Lambda function for handling Alexa
Skill requests that:

-  Use Persistence attributes and Persistence adapter, to store and retrieve
   attributes on AWS DynamoDB table.
-  Demonstrates using a custom slot type.

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
Getting Started documentation. For this sample skill, you need
the ``ASK SDK Standard`` package.

In addition to the SDK, the skill also needs a DynamoDb table. Go to
`AWS Console <https://console.aws.amazon.com>`_
and click on the `DynamoDB <https://console.aws.amazon.com/dynamodb>`_ Service.
In the dashboard, click on 'Create table', provide 'High-Low-Game' as table name
and 'id' as partition key. Leave all settings as default and click 'Create'.

AWS Lambda Setup
~~~~~~~~~~~~~~~~

Refer to
`Hosting a Custom Skill as an AWS Lambda Function <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html>`__
reference for a walkthrough on creating a AWS Lambda function with the
correct role for your skill. When creating the function, select the
"Author from scratch" option, and select Python 2.7 or Python 3.6 runtime.

To prepare the skill for upload to AWS Lambda, create a zip file that
contains `high_low_game.py <high_low_game.py>`_, the SDK and it's dependencies. Make sure to
compress all files directly, **NOT** the project folder. You can check the
AWS Lambda docs to get more information on
`creating a deployment package <https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html>`_.

Once you’ve created your AWS Lambda function and configured "Alexa
Skills Kit" as a trigger, upload the ZIP file produced in the previous
step and set the handler to the fully qualified class name of your
handler function.  In this example, it would be ``high_low_game.handler``.
Finally, copy the ARN for your AWS Lambda function
because you’ll need it when configuring your skill in the Amazon
Developer console.

Alexa Skill Setup
~~~~~~~~~~~~~~~~~

Now that the skill code has been uploaded to AWS Lambda we’re ready to
configure the skill with Alexa. First, navigate to the
`Alexa Skills Kit Developer Console <https://developer.amazon.com/alexa/console/ask>`__.
Click the "Create Skill" button in the upper right. Enter "HighLowGame"
as your skill name. On the next page, select "Custom" and click "Create
skill".

Now we’re ready to define the interaction model for the skill. Under
"Invocation" tab on the left side, define your Skill Invocation Name to
be ``high low game``.

Now it’s time to add the required intents to the skill. Copy the
interactionSchema JSON provided in the `speech_assets <speech_assets/>`_ folder
and paste it under the "JSON Editor" tab. Alternatively, you can also upload
the JSON to the JSON Editor.

.. code:: json

  {
      "interactionModel": {
            "languageModel": {
                "invocationName": "high low game",
                "intents": [
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
                        "name": "AMAZON.YesIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.FallbackIntent",
                        "samples": []
                    },
                    {
                        "name": "AMAZON.NoIntent",
                        "samples": []
                    },
                    {
                        "name": "NumberGuessIntent",
                        "slots": [
                            {
                                "name": "number",
                                "type": "AMAZON.NUMBER"
                            }
                        ],
                        "samples": [
                            "{number}",
                            "is it {number}",
                            "how about {number}",
                            "could be {number}"
                        ]
                    }
                ],
                "types": []
            }
        }
    }

As can be observed from the JSON, we add the built-in **AMAZON.YesIntent**,
**AMAZON.NoIntent** and a custom **NumberGuessIntent**. The
**NumberGuessIntent** is for providing utterances for guessing the number. The
"Yes" and "No" intents are for skill users to confirm if they want to play
the game.

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
