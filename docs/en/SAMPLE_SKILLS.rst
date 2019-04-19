=======================
Sample Skills
=======================

This section provides sample skills that demonstrate the usage of ASK SDK for
Python to build engaging Alexa Skills.

`Hello World (using Classes) <https://github.com/alexa/skill-sample-python-helloworld-classes>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This code sample will allow you to hear a response from Alexa when you
trigger it. It is a minimal sample to get you familiarized with the
Alexa Skills Kit and AWS Lambda.
This sample shows how to create a skill using the Request Handler
classes. For more information, check the `Request Processing <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/REQUEST_PROCESSING.html>`_ documentation.

`Hello World (using Decorators) <https://github.com/alexa/skill-sample-python-helloworld-decorators>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This code sample will allow you to hear a response from Alexa when you
trigger it. It is a minimal sample to get you familiarized with the
Alexa Skills Kit and AWS Lambda.
This sample shows how to create a skill
using the Request Handler Decorators. For more information, check the
`Request Processing <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/REQUEST_PROCESSING.html>`_ documentation.

`Color Picker <https://github.com/alexa/skill-sample-python-colorpicker>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a step-up in functionality from Hello World. When the user provides
their favorite color, Alexa remembers it and tells the user their favorite
color.
It allows you to
capture input from your user and demonstrates the use of Slots. It also
demonstrates use of session attributes and request, response interceptors.

`Fact <https://github.com/alexa/skill-sample-python-fact>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic fact skill. You’ll provide a list of interesting facts
about a topic, Alexa will select a fact at random and tell it to the user
when the skill is invoked.
Demonstrates use of multiple locales and internationalization in the skill.

`Quiz Game <https://github.com/alexa/skill-sample-python-quiz-game>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic quiz game skill. Alexa quizzes the user with facts from
a list you provide.
Demonstrates use of render template directives to support displays on
Alexa-enabled devices with a screen.

`Device Address <https://github.com/alexa/alexa-skills-kit-sdk-for-python/tree/master/samples/GetDeviceAddress>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample skill that shows how to request and access the configured address in
the user’s device settings.
Demonstrates how to use the alexa APIs using the SDK. For more information,
check the documentation on `Alexa Service Clients <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html>`_

`Fact with In-Skill Purchases <https://github.com/alexa/skill-sample-python-fact-in-skill-purchases>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample fact skill with `in-skill purchase <https://developer.amazon.com/docs/in-skill-purchase/isp-overview.html>`_
features, by offering different packs of facts behind a purchase, and a
subscription to unlock all of the packs at once.
Demonstrates calling monetization alexa service and using ASK CLI to enable
in-skill purchasing.

`City Guide <https://github.com/alexa/skill-sample-python-city-guide>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a local recommendations skill. Alexa uses the data that you
provide to offer recommendations according to the user's stated preferences.
Demonstrates calling external APIs from the skill.

`Pet Match <https://github.com/alexa/skill-sample-python-petmatch>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample skill that matches the user with a pet. Alexa prompts the user for
the information it needs to determine a match. Once all of the required
information is collected, the skill sends the data to an external web service
that processes the data and returns the match.
Demonstrates how to prompt and parse multiple values from customers using
`Dialog Management <https://developer.amazon.com/alexa-skills-kit/dialog-management>`_
and `Entity Resolution <https://developer.amazon.com/docs/custom-skills/define-synonyms-and-ids-for-slot-type-values-entity-resolution.html>`_.

`High Low Game <https://github.com/alexa/skill-sample-python-highlowgame>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template for a basic high-low game skill. When the user guesses a number,
Alexa tells the user whether the number she has in mind is higher or lower.
Demonstrates use of persistence attributes and the persistence adapter
in the SDK.

`AudioPlayer SingleStream and MultiStream <https://github.com/alexa/skill-sample-python-audio-player>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sample skills that show how to use `AudioPlayer interface <https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-audioplayer-interface-reference>`__ and `PlaybackController interface <https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-playbackcontroller-interface-reference>`__
in Alexa, to build audioplayer skills. The SingleStream skill sample demonstrates how to create a live radio skill, 
along with localization support. The MultiStream skill sample demonstrates how to create 
a basic podcast skill that can play multiple, pre-recorded audio streams.

`Pager Karaoke <https://github.com/alexa-labs/skill-sample-python-pager-karaoke>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This sample demonstrates 3 features of APL: the
`Pager Component <https://developer.amazon.com/docs/alexa-presentation-language/apl-pager.html>`__,
`SpeakItem Command <https://developer.amazon.com/docs/alexa-presentation-language/apl-standard-commands.html#speakitem-command>`__,
and accessing `device characteristics <https://developer.amazon.com/docs/alexa-presentation-language/apl-viewport-characteristics.html>`__
in the skill code.

