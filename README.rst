.. raw:: html

    <embed>
        <p align="center">
          <img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/avs/docs/ux/branding/mark1._TTH_.png">
          <br/>
          <h1 align="center">Alexa Skills Kit SDK for Python</h1>
          <p align="center">
            <a href="https://travis-ci.org/alexa/alexa-skills-kit-sdk-for-python"><img src="https://img.shields.io/travis/alexa/alexa-skills-kit-sdk-for-python/master.svg?style=flat"></a>
            <a href="https://alexa-skills-kit-python-sdk.readthedocs.io"><img src="https://img.shields.io/readthedocs/alexa-skills-kit-python-sdk.svg?style=flat"></a>
            <a href="https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
            <a href="https://pypi.python.org/pypi/ask-sdk/"><img src="http://img.shields.io/pypi/v/ask-sdk.svg?style=flat"></a>
            <a href="https://pypi.org/project/ask-sdk-core/"><img src="https://pepy.tech/badge/ask-sdk-core"></a>
            <a hreg="https://pypi.python.org/pypi/ask-sdk/"><img src="https://img.shields.io/pypi/pyversions/ask-sdk.svg?style=flat"></a>
          </p>
        </p>
    </embed>

`English <README.rst>`_ |  `日本語 <README.ja.rst>`_

The **ASK SDK for Python** makes it easier for you to build highly engaging skills,
by allowing you to spend more time on implementing features and less on writing
boiler-plate code.


.. |Build Status| image:: https://img.shields.io/travis/alexa-labs/alexa-skills-kit-sdk-for-python/master.svg?style=flat
    :target: https://travis-ci.org/alexa-labs/alexa-skills-kit-sdk-for-python
    :alt: Build Status
.. |Docs| image:: https://img.shields.io/readthedocs/alexa-skills-kit-python-sdk.svg?style=flat
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io
    :alt: Read the docs
.. |Runtime Version| image:: http://img.shields.io/pypi/v/ask-sdk-runtime.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-runtime/
    :alt: Version
.. |Runtime Downloads| image:: https://pepy.tech/badge/ask-sdk-runtime
    :target: https://pepy.tech/project/ask-sdk-runtime
    :alt: Downloads
.. |Core Version| image:: http://img.shields.io/pypi/v/ask-sdk-core.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-core/
    :alt: Version
.. |Core Downloads| image:: https://pepy.tech/badge/ask-sdk-core
    :target: https://pepy.tech/project/ask-sdk-core
    :alt: Downloads
.. |DynamoDb Version| image:: http://img.shields.io/pypi/v/ask-sdk-dynamodb-persistence-adapter.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-dynamodb-persistence-adapter/
    :alt: Version
.. |DynamoDb Downloads| image:: https://pepy.tech/badge/ask-sdk-dynamodb-persistence-adapter
    :target: https://pepy.tech/project/ask-sdk-dynamodb-persistence-adapter
    :alt: Downloads
.. |Standard Version| image:: http://img.shields.io/pypi/v/ask-sdk.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk/
    :alt: Version
.. |Standard Downloads| image:: https://pepy.tech/badge/ask-sdk
    :target: https://pepy.tech/project/ask-sdk
    :alt: Downloads
.. |Webservice Version| image:: http://img.shields.io/pypi/v/ask-sdk-webservice-support.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-webservice-support/
    :alt: Version
.. |Webservice Downloads| image:: https://pepy.tech/badge/ask-sdk-webservice-support
    :target: https://pepy.tech/project/ask-sdk-webservice-support
    :alt: Downloads
.. |Flask Sdk Version| image:: http://img.shields.io/pypi/v/flask-ask-sdk.svg?style=flat
    :target: https://pypi.python.org/pypi/flask-ask-sdk/
    :alt: Version
.. |Flask Sdk Downloads| image:: https://pepy.tech/badge/flask-ask-sdk
    :target: https://pepy.tech/project/flask-ask-sdk
    :alt: Downloads
.. |Django Sdk Version| image:: http://img.shields.io/pypi/v/django-ask-sdk.svg?style=flat
    :target: https://pypi.python.org/pypi/django-ask-sdk/
    :alt: Version
.. |Django Sdk Downloads| image:: https://pepy.tech/badge/django-ask-sdk
    :target: https://pepy.tech/project/django-ask-sdk
    :alt: Downloads
.. |License| image:: http://img.shields.io/pypi/l/ask-sdk-core.svg?style=flat
    :target: https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/LICENSE
    :alt: License
    
Package Versions
----------------
====================================   ==================
Package                                Version
------------------------------------   ------------------
ask-sdk-runtime                        |Runtime Version| |Runtime Downloads|
ask-sdk-core                           |Core Version| |Core Downloads|
ask-sdk-dynamodb-persistence-adapter   |DynamoDb Version| |DynamoDb Downloads|
ask-sdk                                |Standard Version| |Standard Downloads|
ask-sdk-webservice-support (Beta)      |Webservice Version| |Webservice Downloads|
flask-ask-sdk (Beta)                   |Flask Sdk Version| |Flask Sdk Downloads|
django-ask-sdk (Beta)                  |Django Sdk Version| |Django Sdk Downloads|
====================================   ==================


Technical Documentation
-----------------------

========================================================================== ======
Language                                                                   Docs
========================================================================== ======
`English <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/>`_ |English Docs|
`日本語 <https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/>`_   |Japanese Docs|
========================================================================== ======

.. |English Docs| image:: https://readthedocs.org/projects/alexa-skills-kit-python-sdk/badge/?version=latest
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/?badge=latest
    :alt: Read the docs english
    
.. |Japanese Docs| image:: https://readthedocs.org/projects/alexa-skills-kit-python-sdk-japanese/badge/?version=latest
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/?badge=latest
    :alt: Read the docs japanese

`Models <https://github.com/alexa/alexa-apis-for-python>`__
-------

The SDK works on model classes rather than native Alexa JSON requests and
responses. These model classes are generated using the Request, Response JSON
schemas from the `developer docs <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html>`__.

The documentation for the model classes can be found `here <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/models/ask_sdk_model.html>`__.

Samples
-------

`Hello World (using Classes) <https://github.com/alexa/skill-sample-python-helloworld-classes>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This code sample will allow you to hear a response from Alexa when you
trigger it. It is a minimal sample to get you familiarized with the
Alexa Skills Kit and AWS Lambda.

This sample shows how to create a skill
using the Request Handler classes. For more information, check the
`Request Processing <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/REQUEST_PROCESSING.html>`_ documentation.

`Hello World (using Decorators) <https://github.com/alexa/skill-sample-python-helloworld-decorators>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This code sample will allow you to hear a response from Alexa when you
trigger it. It is a minimal sample to get you familiarized with the
Alexa Skills Kit and AWS Lambda.

This sample shows how to create a skill
using the Request Handler Decorators. For more information, check the
`Request Processing <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/REQUEST_PROCESSING.html>`_ documentation.

`Color Picker <https://github.com/alexa/skill-sample-python-colorpicker>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a step-up in functionality from Hello World. When the user provides
their favorite color, Alexa remembers it and tells the user their favorite
color.

It allows you to
capture input from your user and demonstrates the use of Slots. It also
demonstrates use of session attributes and request, response interceptors.

`Fact <https://github.com/alexa/skill-sample-python-fact>`_
~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic fact skill. You’ll provide a list of interesting facts
about a topic, Alexa will select a fact at random and tell it to the user
when the skill is invoked.

Demonstrates use of multiple locales and internationalization in the skill.

`Quiz Game <https://github.com/alexa/skill-sample-python-quiz-game>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic quiz game skill. Alexa quizzes the user with facts from
a list you provide.

Demonstrates use of render template directives to support displays on
Alexa-enabled devices with a screen.

`Device Address <samples/GetDeviceAddress>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample skill that shows how to request and access the configured address in
the user’s device settings.

Demonstrates how to use the alexa APIs using the SDK. For more information,
check the documentation on `Alexa Service Clients <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html>`_

`Fact with In-Skill Purchases <https://github.com/alexa/skill-sample-python-fact-in-skill-purchases>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample fact skill with `in-skill purchase <https://developer.amazon.com/docs/in-skill-purchase/isp-overview.html>`_
features, by offering different packs of facts behind a purchase, and a
subscription to unlock all of the packs at once.

Demonstrates calling monetization alexa service and using ASK CLI to enable
in-skill purchasing.

`City Guide <https://github.com/alexa/skill-sample-python-city-guide>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a local recommendations skill. Alexa uses the data that you
provide to offer recommendations according to the user's stated preferences.

Demonstrates calling external APIs from the skill.

`Pet Match <https://github.com/alexa/skill-sample-python-petmatch>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample skill that matches the user with a pet. Alexa prompts the user for
the information it needs to determine a match. Once all of the required
information is collected, the skill sends the data to an external web service
that processes the data and returns the match.

Demonstrates how to prompt and parse multiple values from customers using
`Dialog Management <https://developer.amazon.com/alexa-skills-kit/dialog-management>`_
and `Entity Resolution <https://developer.amazon.com/docs/custom-skills/define-synonyms-and-ids-for-slot-type-values-entity-resolution.html>`_.

`High Low Game <https://github.com/alexa/skill-sample-python-highlowgame>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic high-low game skill. When the user guesses a number,
Alexa tells the user whether the number she has in mind is higher or lower.

Demonstrates use of persistence attributes and the persistence adapter
in the SDK.

`Audio Player <https://github.com/alexa/skill-sample-python-audio-player>`_
~~~~~~~~~~~~~~~~~~

Project that demonstrates how to use `AudioPlayer interface <https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-audioplayer-interface-reference>`__ and `PlaybackController interface <https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-playbackcontroller-interface-reference>`__ for building audioplayer skills in Alexa. The SingleStream skill sample demonstrates how to create a live radio skill, along with localization support. The MultiStream skill sample demonstrates how to create a basic podcast skill that can play multiple, pre-recorded audio streams.

`Pager Karaoke <https://github.com/alexa-labs/skill-sample-python-pager-karaoke>`__
~~~~~~~~~~~~~~~

This sample demonstrates 3 features of APL: the `Pager Component <https://developer.amazon.com/docs/alexa-presentation-language/apl-pager.html>`__, `SpeakItem Command <https://developer.amazon.com/docs/alexa-presentation-language/apl-standard-commands.html#speakitem-command>`__, and accessing `device characteristics <https://developer.amazon.com/docs/alexa-presentation-language/apl-viewport-characteristics.html>`__ in the skill code.


Alexa Capabilities supported by SDK
-----------------------------------

* `Amazon Pay <https://developer.amazon.com/docs/amazon-pay/integrate-skill-with-amazon-pay.html>`__

* `Audio Player <https://developer.amazon.com/docs/custom-skills/audioplayer-interface-reference.html>`__

* `Display – Body templates for devices with a screen <https://developer.amazon.com/docs/custom-skills/create-skills-for-alexa-enabled-devices-with-a-screen.html>`__

* `Gadgets\Game Engine – Echo Buttons <https://developer.amazon.com/docs/custom-skills/game-engine-interface-reference.html>`__

* `Directive Service (Progressive Response) <https://developer.amazon.com/docs/custom-skills/send-the-user-a-progressive-response.html>`__

* `Messaging <https://developer.amazon.com/docs/smapi/send-a-message-request-to-a-skill.html>`__

* `Monetization <https://developer.amazon.com/alexa-skills-kit/make-money>`__

* `Video <https://developer.amazon.com/docs/custom-skills/videoapp-interface-reference.html>`__

* `Device Address <https://developer.amazon.com/docs/custom-skills/device-address-api.html>`__

* `Lists <https://developer.amazon.com/docs/custom-skills/access-the-alexa-shopping-and-to-do-lists.html#alexa-lists-access>`__

* `Request for customer contact information <https://developer.amazon.com/docs/smapi/alexa-settings-api-reference.html>`__

* `Obtain customer settings information <https://developer.amazon.com/docs/smapi/alexa-settings-api-reference.html>`_

* `Account Linking <https://developer.amazon.com/docs/account-linking/understand-account-linking.html>`__

* `Entity Resolution <https://developer.amazon.com/docs/custom-skills/define-synonyms-and-ids-for-slot-type-values-entity-resolution.html>`__

* `Dialog Management <https://developer.amazon.com/docs/custom-skills/dialog-interface-reference.html>`__

* `Location Services <https://developer.amazon.com/docs/custom-skills/location-services-for-alexa-skills.html>`__

* `Reminders <https://developer.amazon.com/docs/smapi/alexa-reminders-overview.html>`__

* `Proactive Events <https://developer.amazon.com/docs/smapi/proactive-events-api.html>`__

* `Dynamic Entities <https://developer.amazon.com/docs/custom-skills/use-dynamic-entities-for-customized-interactions.html>`__

* `Skill Messaging <https://developer.amazon.com/docs/smapi/skill-messaging-api-reference.html>`__

* `Connections <https://developer.amazon.com/blogs/alexa/post/7b332b32-893e-4cad-be07-a5877efcbbb4/skill-connections-preview-now-skills-can-work-together-to-help-customers-get-more-done>`__

Preview
~~~~~~~

* `Alexa Presentation Language <https://developer.amazon.com/docs/alexa-presentation-language/apl-overview.html>`__

* `Name-free Interactions <https://developer.amazon.com/docs/custom-skills/understand-name-free-interaction-for-custom-skills.html>`_


Hosting Skills on Non-Lambda Resources
--------------------------------------

SDK provides ``ask-sdk-webservice-support`` package, that allows hosting
skills as custom web services. It also provides framework specific adapters
under ``flask-ask-sdk`` and ``django-ask-sdk`` packages, to integrate
skills on the respective frameworks and deploy as web service.

More information on how to use these packages can be found on this
`documentation link <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/WEBSERVICE_SUPPORT.html>`__.

.. warning::

    These features are currently in **Beta**. The interface might change when
    the features are released as stable.


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for
  `existing issues <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`_
  before opening a new one. It would also be helpful if you follow the
  templates for issue and pull request creation.
  Please follow the `contributing guidelines <CONTRIBUTING.md>`_ for
  pull requests!!
- Request and vote for
  `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!
  Remember to select the category as **ASK SDK** if your feature request is
  specific to SDK.


Additional Resources
--------------------

Other Language Alexa Skills Kit SDKs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <embed>
        <div>
            <p><a href="https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs"><img src="https://github.com/konpa/devicon/blob/master/icons/nodejs/nodejs-original.svg?sanitize=true" width="25px" /> Alexa Skills Kit SDK for NodeJS</a></p>
            <p><a href="https://github.com/amzn/alexa-skills-kit-java"><img src="https://github.com/konpa/devicon/raw/master/icons/java/java-original.svg?sanitize=true" width="25px" /> Alexa Skills Kit SDK for Java</a></p>
        </div>
    </embed>

Community
~~~~~~~~~

-  `Amazon Developer Forums <https://forums.developer.amazon.com/spaces/165/index.html>`_ : Join the conversation!
-  `Hackster.io <https://www.hackster.io/amazon-alexa>`_ - See what others are building with Alexa.

Tutorials & Guides
~~~~~~~~~~~~~~~~~~

-  `Voice Design Guide <https://developer.amazon.com/designing-for-voice/>`_ -
   A great resource for learning conversational and voice user interface design.

