.. raw:: html

    <embed>
        <p align="center">
          <img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/avs/docs/ux/branding/mark1._TTH_.png">
          <br/>
          <h1 align="center">Alexa Skills Kit SDK for Python (Beta)</h1>
          <p align="center">
            <a href="https://travis-ci.org/alexa-labs/alexa-skills-kit-sdk-for-python"><img src="https://img.shields.io/travis/alexa-labs/alexa-skills-kit-sdk-for-python/master.svg?style=flat"></a>
            <a href="https://alexa-skills-kit-python-sdk.readthedocs.io"><img src="https://img.shields.io/readthedocs/alexa-skills-kit-python-sdk.svg?style=flat"></a>
            <a href="https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
            <a href="https://pypi.python.org/pypi/ask-sdk/"><img src="http://img.shields.io/pypi/v/ask-sdk.svg?style=flat"></a>
            <a href="https://pypi.org/project/ask-sdk/"><img src="https://pepy.tech/badge/ask-sdk"></a>
            <a hreg="https://pypi.python.org/pypi/ask-sdk/"><img src="https://img.shields.io/pypi/pyversions/ask-sdk.svg?style=flat"></a>
          </p>
        </p>
    </embed>

`English <README.rst>`_ |  `日本語 <README.ja.rst>`_

The **ASK SDK for Python (Beta)** makes it easier for you to build highly engaging skills,
by allowing you to spend more time on implementing features and less on writing
boiler-plate code.


.. |Build Status| image:: https://img.shields.io/travis/alexa-labs/alexa-skills-kit-sdk-for-python/master.svg?style=flat
    :target: https://travis-ci.org/alexa-labs/alexa-skills-kit-sdk-for-python
    :alt: Build Status
.. |Docs| image:: https://img.shields.io/readthedocs/alexa-skills-kit-python-sdk.svg?style=flat
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io
    :alt: Read the docs
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
.. |License| image:: http://img.shields.io/pypi/l/ask-sdk-core.svg?style=flat
    :target: https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/blob/master/LICENSE
    :alt: License

Package Versions
----------------
====================================   ==================
Package                                Version           
------------------------------------   ------------------
ask-sdk-core                           |Core Version| |Core Downloads|
ask-sdk-dynamodb-persistence-adapter   |DynamoDb Version| |DynamoDb Downloads|
ask-sdk                                |Standard Version| |Standard Downloads|
====================================   ==================


Technical Documentation
-----------------------

===========================================================================  ======
Language                                                                     Docs
===========================================================================  ======
`English <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/>`_   |English Docs|
`日本語 <https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/>`_     |Japanese Docs|
===========================================================================  ======

.. |English Docs| image:: https://readthedocs.org/projects/alexa-skills-kit-python-sdk/badge/?version=latest
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/?badge=latest
    :alt: Read the docs english
    
.. |Japanese Docs| image:: https://readthedocs.org/projects/alexa-skills-kit-python-sdk-japanese/badge/?version=latest
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/?badge=latest
    :alt: Read the docs japanese

Models
------

The SDK works on model classes rather than native Alexa JSON requests and
responses. These model classes are generated using the Request, Response JSON
schemas from the `developer docs <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html>`__. The source code for the model classes can be
found `here <https://github.com/alexa-labs/alexa-apis-for-python>`__.

The documentation for the model classes can be found `here <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/models/ask_sdk_model.html>`__.

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
  Please follow the `contributing guidelines <CONTRIBUTING.md>`_ for
  pull requests!!
- Request and vote for
  `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!


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
