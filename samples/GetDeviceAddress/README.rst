Alexa Skills Kit SDK Sample - Get Device Address
================================================

This Alexa sample skill is a template for a basic Alexa Device Address API use.

The Device Address API enables skills to request and access the
configured address in the customer’s device settings. This means you can build
skills with the context to understand the customers who use the skill, then
use the data to customize the voice experience. Your skill, for example,
can deliver food and groceries to a customer’s home or provide directions to
a nearby gym. You can also see where your most active users are.
Check out our
`address information documentation <https://developer.amazon.com/docs/custom-skills/device-address-api.html>`_
to learn more.

There are two levels of location data you can request:

-  Full address, which includes street address, city, state, zip, and country
-  Country and postal code only

This sample uses the first level of location data.

When a user enables a skill that wants to use this location data, the user
will be prompted in the Alexa app to consent to the location data being shared
with the skill. It is important to note that when a user enables a skill
via voice, the user will not be prompted for this information and the
default choice will be "none". In this case, you can use cards to prompt
the user to provide consent using the Alexa app. The skill sample shows this
usecase with ``AskForPermissionsConsentCard`` in the response.


Concepts
--------

This sample shows how to create a Lambda function for handling Alexa
Skill requests that:

-  Use service clients in SDK, to call the Alexa APIs.
   More on `service clients here <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html#>`__
-  Use ``AskForPermissionsConsentCard`` for asking for location consent

Setup
-----

To run this example skill you need to do two things. The first is to
deploy the example code in lambda, and the second is to configure the
Alexa skill to use Lambda.

Prerequisites
~~~~~~~~~~~~~

Please follow the
`prerequisites <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html#prerequisites>`_ section and the
`adding ASK SDK <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html#adding-the-ask-sdk-for-python-to-your-project>`_
section in
Getting Started documentation. For this sample skill, you need
the ``ASK SDK Core`` package.

AWS Lambda Setup
~~~~~~~~~~~~~~~~

Refer to
`Hosting a Custom Skill as an AWS Lambda Function <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html>`__
reference for a walkthrough on creating a AWS Lambda function with the
correct role for your skill. When creating the function, select the
"Author from scratch" option, and select Python 2.7 or Python 3.6 runtime.

To prepare the skill for upload to AWS Lambda, create a zip file that
contains `lambda_function.py <lambda/py/lambda_function.py>`_, the SDK and it's dependencies. Make sure to
compress all files directly, **NOT** the project folder. You can check the
AWS Lambda docs to get more information on
`creating a deployment package <https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html>`_.

Once you’ve created your AWS Lambda function and configured "Alexa
Skills Kit" as a trigger, upload the ZIP file produced in the previous
step. Finally, copy the ARN for your AWS Lambda function
because you’ll need it when configuring your skill in the Amazon
Developer console.

Alexa Skill Setup
~~~~~~~~~~~~~~~~~

Now that the skill code has been uploaded to AWS Lambda we’re ready to
configure the skill with Alexa. First, navigate to the
`Alexa Skills Kit Developer Console <https://developer.amazon.com/alexa/console/ask>`__.
Click the "Create Skill" button in the upper right. Enter "GetDeviceAddress"
as your skill name. On the next page, select "Custom" and click "Create
skill".

Now we’re ready to define the interaction model for the skill. Under
"Invocation" tab on the left side, define your Skill Invocation Name to
be ``device address``.

Now it’s time to add the required intents to the skill. Copy the
interactionSchema JSON provided in the `models <models/>`_ folder
and paste it under the "JSON Editor" tab. Alternatively, you can also upload
the JSON to the JSON Editor.

.. code:: json

  {
    "interactionModel": {
        "languageModel": {
            "invocationName": "device address",
            "intents": [
                {
                    "name": "GetAddressIntent",
                    "slots": [],
                    "samples": [
                        "where am I located",
                        "where do I live",
                        "whats my address",
                        "where am I",
                        "whats my location"
                    ]
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
                }
            ],
            "types": []
        }
    }
  }

As can be observed from the JSON, we add a custom **GetAddressIntent** for
providing utterances for invoking the device address API call.

Once you’re done editing the interaction model don’t forget to save and
build the model.

Let’s move on to the skill configuration section. Under "Endpoint"
select "AWS Lambda ARN" and paste in the ARN of the function you created
previously. The rest of the settings can be left at their default
values. Click "Save Endpoints" and proceed to the next section.

Under the AWS lambda function "Alexa Skills Kit" trigger, enable the "Skill Id
verification" and provide the Skill Id from the skill endpoint screen. Save
the lambda function.

Since the skill needs to ask for Device Address permission from the user, this
needs to be configured in the skill. Click the "Permissions" tab on the left
navigation pane, enable the ``Device Address`` permission and select the
``Full Address`` radio button.

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

-  `Official Alexa Skills Kit Python SDK Docs <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/>`_
-  `Official Alexa Skills Kit Docs <https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html>`_
