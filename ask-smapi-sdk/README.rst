==========================================================
ASK SMAPI SDK - Alexa Skills Management API Python Library
==========================================================

``ask-smapi-sdk`` is the Python library package for Alexa
Skill Management API (SMAPI). SMAPI is a set of API
operations that allow you to programmatically manage
and test Alexa skills and related resources such as
interaction models. More information on SMAPI can be
found at `Alexa Developer Documentation <https://developer.amazon.com/docs/smapi/smapi-overview.html>`__.

Quick Start
-----------

Install ASK SMAPI SDK
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ pip install ask-smapi-sdk

Install NPM and ASK CLI
~~~~~~~~~~~~~~~~~~~~~~~
- Install NPM using the instructions provided `here <https://www.npmjs.com/get-npm>`__.
- This is needed to get started with the ASK CLI, which will be used to generate
  Login with Amazon tokens you will need to access SMAPI.

Assuming that you have ``npm`` installed, you can install the ASK CLI
from NPM as follows:

.. code-block:: sh

    $ npm install ask-cli -g

Generate Login with Amazon Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Create a new security profile for your Amazon Developer account by following the instructions
  provided `here <https://developer.amazon.com/docs/smapi/ask-cli-command-reference.html#generate-lwa-tokens>`__.
- This will generate ``Client ID`` and ``Client Secret`` keys.
- Using the ASK CLI, run: ``ask util generate-lwa-tokens``. You will be asked to provide the ``Client ID``
  and ``Client Secret`` keys from the previous step. This will return the following JSON with a ``Refresh Token``:

.. code-block:: json

    {
      "access_token": "ACCESS_TOKEN",
      "refresh_token": "REFRESH_TOKEN",
      "token_type": "bearer",
      "expires_in": 3600,
      "expires_at": "2019-11-19T20:25:06.584Z"
    }


Configure SMAPI Client
~~~~~~~~~~~~~~~~~~~~~~
Use the ``Client ID``, ``Client Secret`` and ``Refresh Token`` retrieved in the previous step to configure a new SMAPI client:

.. code-block:: python

    from ask_smapi_sdk import StandardSmapiClientBuilder
    smapi_client_builder = StandardSmapiClientBuilder(client_id='Client ID', client_secret='Client Secret Key', refresh_token='Refresh Token')
    smapi_client = smapi_client_builder.client()


Usage Examples
--------------

For the complete list of functions, please see the ASK SMAPI Models documentation.

List Skills
~~~~~~~~~~~
.. code-block:: python

    try:
        result = smapi_client.list_skills_for_vendor_v1(vendor_id='Vendor ID', full_response=True)
        print("==========================================")
        print(result.headers)
        print(result.body)
        print("==========================================")
    except Exception as e:
        print(e.body if hasattr(e, 'body') else e)

Get Skill Manifest
~~~~~~~~~~~~~~~~~~
.. code-block:: python

    try:
        result = smapi_client.get_skill_manifest_v1(skill_id='SKILL ID', stage='SKILL STAGE')
        print("==========================================")
        print(result)
        print("==========================================")
    except Exception as e:
        print(e.body if hasattr(e, 'body') else e)

Documentation
-------------

- `SMAPI SDK Reference Documentation <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/api/smapi.html>`__
- `ASK SMAPI Models Documentation <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/smapi_models/ask_smapi_model.html>`__
- `SMAPI Documentation <https://developer.amazon.com/docs/smapi/smapi-overview.html>`__


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for the `existing issues <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`_ before opening a new one. It would also be helpful
  if you follow the templates for issue and pull request creation. Please follow the `contributing guidelines <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`__
- Request and vote for `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`__
