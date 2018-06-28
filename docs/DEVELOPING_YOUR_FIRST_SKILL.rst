============================
Developing Your First Skill
============================

The `Getting Started <GETTING_STARTED.rst>`_ guide showed how to set up and
install the ASK SDK for Python into a specific directory or into a virtual
environment using virtualenv. This guide walks you through developing your
first skill with the ASK SDK for Python.

Prerequisites
-------------

In addition to an installed version of the ASK SDK for Python you need:

* An `Amazon Developer <https://developer.amazon.com/>`_ account. This is
  required to create and configure Alexa skills.
* An `Amazon Web Services (AWS) <https://aws.amazon.com/>`_ account. This is
  required for hosting a skill on AWS Lambda.

Creating Hello World
--------------------

You'll write your Hello World in a single python file named ``hello_world.py``.
When you upload your code to AWS Lambda, you must include your skill code and
its dependencies inside a zip file as a flat file structure, so you'll place
your code in the same folder as the ASK SDK for Python.

If you set up the SDK in a specific folder, the SDK is installed into
the ask-sdk folder within your skill folder. If you are using a virtual
environment, on Windows the SDK is installed into the ``site-packages`` folder
located inside the ``Lib`` folder. For MacOS/Linux the location depends on
the version of Python you are using, for instance *Python 3.6* users will
find site-packages inside the ``lib/Python3.6`` folder.

Now, in the same folder where the ASK SDK for Python is installed, use your
favorite text editor or IDE to create a file named ``hello_world.py``.

Implementing Hello World
------------------------

Start by creating a skill builder object. The skill builder object helps in
adding components responsible for handling input requests and generating
custom responses for your skill.

Type or paste the following code into your ``hello_world.py`` file.

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

Request handlers
~~~~~~~~~~~~~~~~

A custom skill needs to respond to events sent by the Alexa service.
For instance, when you ask your Alexa device (e.g. Echo, Echo Dot, Echo Show,
etc.) to 'open hello world', your skill needs to respond to the LaunchRequest
that is sent to your Hello World skill. With the ASK SDK for Python, you simply
need to write a request handler, which is code to handle incoming requests and
return a response. Your code is responsible for making sure that the right
request handler is used to process incoming requests and for providing a
response. The ASK SDK for Python provides two ways to create request handlers:

1. Implement the ``AbstractRequestHandler`` class under
``ask_sdk_core.dispatch_components`` package. The class should contain
implementations for ``can_handle`` and ``handle`` methods.
2. Use the request_handler decorator in instantiated skill builder object to
tag functions that act as handlers for different incoming requests.

The implementation of the Hello World skill explores using handler classes
first and then shows how to write the same skill using decorators.
The functionality of these is identical and you can use either.

The completed source code for both options is available in the
`HelloWorld <../samples/HelloWorld>`_ sample folder.


Exception handlers
~~~~~~~~~~~~~~~~~~

Sometimes things go wrong, and your skill code needs a way to handle the problem 
gracefully. The ASK SDK for Python supports exception handling in a similar way 
to handling requests. You have a choice of using handler classes or decorators. 
The following implementation sections explore how to implement exception handling.

Implementation using handler classes
------------------------------------

To use handler classes, each request handler is written as a class that
implements two methods of the ``AbstractRequestHandler`` class; ``can_handle``
and ``handle``.

The ``can_handle`` method returns a Boolean value indicating
if the request handler can create an appropriate response for the request.
The ``can_handle`` method has access to the request type and additional
attributes that the skill may have set in previous requests or even saved
from a previous interaction. The Hello World skill only needs to
reference the request information to decide if each handler can respond to
an incoming request.

LaunchRequest handler
~~~~~~~~~~~~~~~~~~~~~

The following code example shows how to configure a handler to be invoked when
the skill receives a `LaunchRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#launchrequest>`_.
The LaunchRequest event occurs when the skill is invoked without a specific intent.

Type or paste the following code into your ``hello_world.py`` file, after the
previous code.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_model.ui import SimpleCard

    class LaunchRequestHandler(AbstractRequestHandler):
         def can_handle(self, handler_input):
             return handler_input.request_envelope.request.object_type == "LaunchRequest"

         def handle(self, handler_input):
             speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

             handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Hello World", speech_text)).set_should_end_session(
                False)
             return handler_input.response_builder.response

The can_handle function returns **True** if the incoming request is a
LaunchRequest. The handle function generates and returns a basic greeting
response.

HelloWorldIntent handler
~~~~~~~~~~~~~~~~~~~~~~~~

The following code example shows how to configure a handler to be invoked
when the skill receives an intent request with the name HelloWorldIntent.
Type or paste the following code into your ``hello_world.py`` file, after
the previous handler.

.. code-block:: python

    class HelloWorldIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return (handler_input.request_envelope.request.object_type == "IntentRequest"
                    and handler_input.request_envelope.request.intent.name == "HelloWorldIntent")

        def handle(self, handler_input):
            speech_text = "Hello World"

            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Hello World", speech_text)).set_should_end_session(
                True)
            return handler_input.response_builder.response

The can_handle function detects if the incoming request is an
`IntentRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#intentrequest>`_,
and returns **True** if the intent name is HelloWorldIntent. The handle
function generates and returns a basic “Hello World” response.

HelpIntent handler
~~~~~~~~~~~~~~~~~~

The following code example shows how to configure a handler to be invoked
when the skill receives the built-in intent
`AMAZON.HelpIntent <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`_.
Type or paste the following code into your ``hello_world.py file``, after the
previous handler.

.. code-block:: python

    class HelpIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return (handler_input.request_envelope.request.object_type == "IntentRequest"
                    and handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent")

        def handle(self, handler_input):
            speech_text = "You can say hello to me!"

            handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
                SimpleCard("Hello World", speech_text))
            return handler_input.response_builder.response

Similar to the previous handler, this handler matches an IntentRequest with
the expected intent name. Basic help instructions are returned, and ``.ask(speech_text)`` 
causes the user's microphone to open up for the user to respond.

CancelAndStopIntent handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CancelAndStopIntentHandler is similar to the HelpIntent handler, as it
is also triggered by the built-In
`AMAZON.CancelIntent or AMAZON.StopIntent Intents <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`_.
The following example uses a single handler to respond to both intents.
Type or paste the following code into your ``hello_world.py`` file, after the
previous handler.

.. code-block:: python

    class CancelAndStopIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and (handler_input.request_envelope.request.intent.name == "AMAZON.CancelIntent"
                     or handler_input.request_envelope.request.intent.name == "AMAZON.StopIntent"))

        def handle(self, handler_input):
            speech_text = "Goodbye!"

            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Hello World", speech_text))
            return handler_input.response_builder.response

In the above example, ``can_handle`` needs a function to be passed.
``is_intent_name`` returns a function, but we need to check if the request is
either *AMAZON.CancelIntent* or *AMAZON.StopIntent*. We achieve this by
creating an anonymous function on the fly using Python's in-built ``lambda``
function.

The response to both intents is the same, so having a single handler reduces
repetitive code.

SessionEndedRequest handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although you cannot return a response with any speech, card or directives
after receiving a `SessionEndedRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#sessionendedrequest>`_,
the SessionEndedRequestHandler is a good place to put your cleanup logic.
Type or paste the following code into your ``hello_world.py`` file, after the
previous handler.

.. code-block:: python

    class SessionEndedRequestHandler(AbstractRequestHandler):

        def can_handle(self, handler_input):
            return handler_input.request_envelope.request.object_type == "SessionEndedRequest"

        def handle(self, handler_input):
            #any cleanup logic goes here

            return handler_input.response_builder.response

Implementing exception handlers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following sample adds a *catch all* exception handler to your skill, to
ensure the skill returns a meaningful message for all exceptions.
Type or paste the following code into your ``hello_world.py`` file, after the
previous handler.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractExceptionHandler

    class AllExceptionHandler(AbstractExceptionHandler):

        def can_handle(self, handler_input, exception):
            return True

        def handle(self, handler_input, exception):
            # Log the exception in CloudWatch Logs
            print(exception)

            speech = "Sorry, I didn't get it. Can you please say it again!!"
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response

Creating the Lambda handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Lambda handler <https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html>`_
is the entry point for your AWS Lambda function. The following code example
creates a Lambda handler function to route all inbound requests to your skill.
The Lambda handler function creates an SDK skill instance configured with the
request handlers that you just created. Type or paste the following code into
your ``hello_world.py`` file, after the previous handler.

.. code-block:: python

    sb.request_handlers.extend([
        LaunchRequestHandler(),
        HelloWorldIntentHandler(),
        HelpIntentHandler(),
        CancelAndStopIntentHandler(),
        SessionEndedRequestHandler()])

    sb.add_exception_handler(AllExceptionHandler())

    handler = sb.lambda_handler()


Implementation using decorators
-------------------------------

The following code implements the same functionality as above but uses function
decorators. You can think of the decorators as a replacement for the
``can_handle`` method implemented in each request handler above.

To try the skill using this code, make sure that
your ``hello_world.py`` file contains only the following before adding the
handler functions:

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

LaunchRequest handler
~~~~~~~~~~~~~~~~~~~~~

The following code example shows how to configure a handler to be invoked
when the skill receives a
`LaunchRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#launchrequest>`_.
The LaunchRequest event occurs when the skill is invoked without a
specific intent.

Type or paste the following code into your ``hello_world.py`` file, after the
previous code.

.. code-block:: python

    from ask_sdk_core.utils import is_request_type
    from ask_sdk_model.ui import SimpleCard

    @sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
    def launch_request_handler(handler_input):
        speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

        handler_input.response_builder.speak(speech_text).set_card(
             SimpleCard("Hello World", speech_text)).set_should_end_session(
             False)
        return handler_input.response_builder.response


Similar to the ``can_handle`` function for the LaunchRequestHandler in
the Class pattern, the decorator returns **True** if the incoming request is
a LaunchRequest. The ``handle`` function generates and returns a basic
greeting response in the same way the handle function works for the Class
pattern.

HelloWorldIntent handler
~~~~~~~~~~~~~~~~~~~~~~~~

The following code example shows how to configure a handler to be invoked
when the skill receives an intent request with the name HelloWorldIntent.
Type or paste the following code into your ``hello_world.py`` file, after
the previous handler.

.. code-block:: python

    from ask_sdk_core.utils import is_intent_name

    @sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
    def hello_world_intent_handler(handler_input):
        speech_text = "Hello World!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


HelpIntent handler
~~~~~~~~~~~~~~~~~~

The following code example shows how to configure a handler to be invoked
when the skill receives the built-in intent
`AMAZON.HelpIntent <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`_.
Type or paste the following code into your ``hello_world.py file``, after the
previous handler.

.. code-block:: python

    @sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
    def help_intent_handler(handler_input):
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

Similar to the previous handler, this handler matches an IntentRequest with
the expected intent name. Basic help instructions are returned, and ``.ask(speech_text)`` 
causes the user's microphone to open up for the user to respond.


CancelAndStopIntent handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CancelAndStopIntentHandler is similar to the HelpIntent handler, as it
is also triggered by the built-in
`AMAZON.CancelIntent or AMAZON.StopIntent intents <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`_.
The following example uses a single handler to respond to both Intents.
Type or paste the following code into your ``hello_world.py`` file, after the
previous handler.

.. code-block:: python

    @sb.request_handler(
        can_handle_func=lambda input :
            is_intent_name("AMAZON.CancelIntent")(input) or
            is_intent_name("AMAZON.StopIntent")(input))
    def cancel_and_stop_intent_handler(handler_input):
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

In the above example, ``can_handle`` needs a function to be passed.
``is_intent_name`` returns a function, but we need to check if the request is
either *AMAZON.CancelIntent* or *AMAZON.StopIntent*. We achieve this by
creating an anonymous function on the fly using Python's in-built ``lambda``
function.

The response to both intents is the same, so having a single handler reduces
repetitive code.

SessionEndedRequest handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although you cannot return a response with any speech, card or directives
after receiving a `SessionEndedRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#sessionendedrequest>`_,
the SessionEndedRequestHandler is a good place to put your cleanup logic.
Type or paste the following code into your ``hello_world.py`` file, after the
previous handler.

.. code-block:: python

    @sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
    def session_ended_request_handler(handler_input):
        #any cleanup logic goes here

        return handler_input.response_builder.response


Implementing exception handlers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following sample adds a *catch all* exception handler to your skill, to
ensure the skill returns a meaningful message in case of all exceptions.
Type or paste the following code into your ``hello_world.py`` file, after the
previous handler.

.. code-block:: python

    @sb.exception_handler(can_handle_func=lambda i, e: True)
    def all_exception_handler(handler_input, exception):
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


Creating the Lambda handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Lambda handler <https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html>`_
is the entry point for your AWS Lambda function. The following code example
creates a Lambda handler function to route all inbound requests to your skill.
The Lambda Handler function creates an SDK skill instance configured with
the request handlers that you just created.

Type or paste the following code into your ``hello_world.py`` file, after
the previous handler.

.. code-block:: python

    handler = sb.lambda_handler()
    
When using decorators, your request handlers are automatically recognized by 
the Skill Builder object instantiated at the top of the code.

Preparing your code for AWS Lambda
----------------------------------

Your code is now complete and you need to create .zip files that contain the files ready to upload to
Lambda. If you followed the instructions above, create a .zip file of the content of the
folder (not the folder itself) where you created the ``hello_world.py`` file.
Name the file ``skill.zip``. You can check the AWS Lambda docs to get more
information on creating a
`deployment package <https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html>`_.
Before uploading the code to AWS Lambda, you need to create an AWS Lambda
function and create the skill on the Alexa Developer Portal.

Creating an AWS Lambda function
-------------------------------

Refer to `Hosting a Custom Skill as an AWS Lambda Function <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html>`_
for a walkthrough on creating an AWS Lambda function with the correct role for
your skill. When creating the function, select the *Author from scratch* option
and select the ``Python 2.7`` or ``Python 3.6`` runtime.

Once you've created your AWS Lambda function, it's time to give the Alexa
service the ability to invoke it. To do this, navigate to the **Triggers** tabs
in your Lambda's configuration, and add **Alexa Skills Kit** as the trigger
type. Once this is done, upload the ``skill.zip`` file produced in the previous step
and fill in the *handler* information with module_name.handler which is
``hello_world.handler`` for this example.

Configuring and testing Your skill
----------------------------------

Now that the skill code has been uploaded to AWS Lambda, you can configure
the skill with Alexa.

* Create a new skill by following these steps:

  1. Log in to the `Alexa Skills Kit Developer Console <https://developer.amazon.com/alexa/console/ask>`_.
  2. Click the **Create Skill** button in the upper right.
  3. Enter “HelloWorld” as your skill name and click Next.
  4. For the model, select **Custom** and click **Create skill**.

* Next, define the interaction model for the skill. Select the **Invocation**
  option from the sidebar and enter "greeter" for the **Skill Invocation Name**.

* Next, add an intent called ``HelloWorldIntent`` to the interaction model. Click
  the **Add** button under the
  Intents section of the Interaction Model. Leave "**Create custom intent**"
  selected, enter "**HelloWorldIntent**" for the intent name, and create the
  intent. On the intent detail page, add some sample utterances that users can
  say to invoke the intent. For this example, consider the following
  sample utterances, and feel free to add others.

  ::

      say hello
      say hello world
      hello
      say hi
      say hi world
      hi
      how are you


* Since ``AMAZON.CancelIntent``, ``AMAZON.HelpIntent``, and ``AMAZON.StopIntent`` are
  built-in Alexa intents, you do not need to provide sample utterances for them.

* The Developer Console allows you to edit the entire skill model in JSON
  format. Select **JSON Editor** from the sidebar. For this sample, you can use
  the following JSON schema.

  .. code-block:: json

      {
        "interactionModel": {
          "languageModel": {
            "invocationName": "greeter",
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
                "name": "HelloWorldIntent",
                "slots": [],
                "samples": [
                  "how are you",
                  "hi",
                  "say hi world",
                  "say hi",
                  "hello",
                  "say hello world",
                  "say hello"
                ]
              }
            ],
            "types": []
          }
        }
      }


* Once you are done editing the interaction model, be sure to save and build
  the model.

* Next, configure the endpoint for the skill. To do this, follow these steps:

  1. Under your skill, click the **Endpoint** tab, select AWS Lambda ARN, 
     and copy the **Skill ID** of the skill you just created.
  2. Open the AWS Developer Console in a new tab.
  3. Navigate to the AWS Lambda function created in the previous step.
  4. From the **Designer** menu, add the **Alexa Skills Kit** trigger menu, and 
     scroll down to paste the skill ID into the **Skill ID Verification** configuration. 
     Click **Add and save** once completed to update the AWS Lambda function.
  5. Copy the AWS Lambda function **ARN** from the top right corner of the page. 
     An ARN is a unique resource number that helps Alexa service identify the 
     AWS Lambda function it needs to call during skill invocation.
  6. Navigate to the Alexa Skills Kit Developer Console, and click on your
     **HelloWorld** skill.
  7. Under your skill, click **Endpoint** tab, select **AWS Lambda ARN** and
     paste in the ARN under **Default Region** field.
  8. The rest of the settings can be left at their default values.
     Click **Save Endpoints**.
  9. Click **Invocation** tab, save and build the model.

* At this point you can test the skill. In the top navigation, click **Test**. 
  Make sure that the **Test is enabled for this skill**
  option is enabled. You can use the Test page to simulate requests, in text
  and voice form.

* Use the invocation name along with one of the sample utterances as a guide. 
  For example, *tell greeter to say hello* should result
  in your skill responding with “Hello World” voice and "Hello World" card on
  devices with display. You can also open the Alexa app on your phone or at 
  https://alexa.amazon.com) and see your skill listed under **Your Skills**.

* Feel free to start experimenting with your intents as well as
  the corresponding request handlers in your skill's code. Once you're finished
  iterating, optionally move on to getting your skill certified and published 
  so it can be used by customers worldwide.
