========================================================
ASK SDK S3 Adapter of Python ASK SDK
========================================================

ask-sdk-s3-persistence-adapter is the persistence adapter package for Alexa Skills Kit (ASK) by
the Software Development Kit (SDK) team for Python. It has the persistence adapter implementation
for connecting the Skill to the AWS S3.

Note
-----
Because Amazon S3 provides `eventual consistency <https://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.html>`_ for updates to existing objects, we recommend using
`ask-sdk-dynamodb-persistence-adapter <https://github.com/alexa/alexa-skills-kit-sdk-for-python/tree/master/ask-sdk-dynamodb-persistence-adapter>`_ for persistent attributes if your skill requires read-after-write consistency.


Quick Start
-----------

Installation
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, you can
install the package and it's dependencies (``ask-sdk-model``, ``ask-sdk-core``) from PyPi
as follows:

.. code-block:: sh

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install ask-sdk-s3-persistence-adapter


You can also install the whole s3 persistence adapter package locally by following these steps:

.. code-block:: sh

    $ git clone https://github.com/alexa/alexa-skills-kit-sdk-for-python.git
    $ cd alexa-skills-kit-sdk-for-python/ask-sdk-s3-persistence-adapter
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ python setup.py install


Usage and Getting Started
-------------------------

Getting started guides, SDK Features, API references, samples etc. can
be found at `Read The Docs <https://developer.amazon.com/docs/alexa-skills-kit-sdk-for-python/overview.html>`_


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for the `existing issues <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`_ before opening a new one. It would also be helpful
  if you follow the templates for issue and pull request creation. Please follow the `contributing guidelines <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`_!!
- Request and vote for `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!