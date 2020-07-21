==================================================
ASK SDK Local debug - Debugger for Python ASK SDK
==================================================

**ASK SDK Local Debug** (`ask-sdk-local-debug`) is a package which enables you to test your skill code locally against your skill invocations
by routing requests to your developer machine. This enables you to verify changes quickly to skill code as you
can test without needing to deploy skill code to Lambda.

.. note::

    This feature is currently only available to customers in the `NA region <https://developer.amazon.com/en-US/docs/alexa/custom-skills/develop-skills-in-multiple-languages.html#h2-multiple-endpoints>`__.


Quick Start
-----------

Installation
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, you can
install the package from PyPi as follows:

.. code-block:: sh

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install ask-sdk-local-debug


You can also install the package locally by following these steps:

.. code-block:: sh

    $ git clone https://github.com/alexa/alexa-skills-kit-sdk-for-python.git
    $ cd alexa-skills-kit-sdk-for-python/ask-sdk-local-debug
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ python setup.py install


Usage and Getting Started
-------------------------

Using Alexa SKills toolkit for VSCode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Alexa Skills Toolkit for Visual Studio <https://developer.amazon.com/en-US/docs/alexa/ask-toolkit/get-started-with-the-ask-toolkit-for-visual-studio-code.html>`__
offer integrated support for local debugging. To get started, please review our technical documentation on
how to `Test your local Alexa skill <https://developer.amazon.com/en-US/docs/alexa/ask-toolkit/vs-code-ask-skills.html#test>`__ using VSCode.


.. note::

    If you have existing an `ASK CLI` profile, you will need to sign in again using the latest version of ASK CLI (>=2.13).
    Once installed, simply re-run `ask configure` to re-authorize your profile for local debugging.


Using with other IDEs and Debuggers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- To instantiate a connection to the local debugging service, retrieve the following details for your skill :
    - **ACCESS_TOKEN** :
        1. Install `ASK CLI v2 <https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html>`__.

        .. code-block:: sh

            npm install ask-cli@2 -g

        2. Generate the accessToken using ASK CLI

        .. code-block:: sh

            ask util generate-lwa-tokens --scopes alexa::ask:skills:debug

        3. You will be directed to a Login with Amazon page. Sign in and retrieve your ACCESS_TOKEN from the terminal.

    - **SKILL_ID** : The ID of the skill you are trying to debug. Ensure that the developer account you used to login to obtain the access token has access to this skill.
    - **HANDLER_NAME** : The exported handler method (typically `lambda_handler` or `handler`). For example, please see the `Hello world example <https://github.com/alexa/skill-sample-python-helloworld-classes/blob/master/lambda/py/hello_world.py#L198>`__.
    - **FILE_NAME** : The path to your skill code's main file (typically `lambda_function.py`). This file or module contains the skill's handler function.

- Create a `local_debug.py` file in your skill's lambda directory and add the following code :

    .. code-block:: python

        from ask_sdk_local_debug.local_debugger_invoker import LocalDebuggerInvoker

        if __name__ == "__main__":
            LocalDebuggerInvoker([
                '--accessToken', '<ACCESS_TOKEN>',
                '--skillId', '<SKILL_ID>',
                '--skillHandler', 'HANDLER_NAME',
                '--skillFilePath', '<FILE_NAME>']
            ).invoke()

- Configure your preferred IDE or other debugging tool to attach to the above process or execute directly from your preferred IDE. For example, in VS Code, this would be included in the launch.json:

    .. code-block:: json

        {
           "type": "python",
           "request": "launch",
           "name": "Skill Debug",
           "program": "<Absolute file path to local_debug.py>",
           "args": [
                "--accessToken", "<AccessToken>",
                "--skillId", "<SkillId>",
                "--skillHandler", "<HandlerName>",
                "--skillFilePath", "<SkillFilePath>"
            ]
        }

Things to note
--------------

1. Local debugging is only available for a skill’s *development* stage.
2. A connection remains active for **1 hour**. You will need to reinstantiate the connection after 1 hour.
3. All Alexa requests for the skill will be routed to your development machine while the connection is active.
4. Only one connection session may be active for a given Skill ID and developer account.


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for the `existing issues <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`_ before opening a new one. It would also be helpful
  if you follow the templates for issue and pull request creation. Please follow the `contributing guidelines <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`_!
- Request and vote for `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!
