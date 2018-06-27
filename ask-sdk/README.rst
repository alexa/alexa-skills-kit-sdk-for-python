========================================================
ASK SDK - Standard / Full distribution of Python ASK SDK
========================================================

ask-sdk is the standard SDK package for Alexa Skills Kit (ASK) by
the Software Development Kit (SDK) team for Python. It is a *all batteries included*
package for developing Alexa Skills.


Quick Start
-----------

Installation
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, you can
install the package and it's dependencies (``ask-sdk-model``, ``ask-sdk-core``,
``ask-sdk-dynamodb-persistence-adapter``) from PyPi
as follows:

.. code-block:: sh

    >>> virtualenv venv
    >>> . venv/bin/activate
    >>> pip install ask-sdk


You can also install the whole standard package locally by following these steps:

.. code-block:: sh

    >>> git clone https://github.com/alexalabs/alexa-skills-kit-for-python-sdk.git
    >>> cd alexa-skills-kit-for-python-sdk/ask-sdk
    >>> virtualenv venv
    ...
    >>> . venv/bin/activate
    >>> python setup.py install


Usage and Getting Started
-------------------------
A Getting Started guide can be found `here <../docs/GETTING_STARTED.rst>`_


Got Feedback?
-------------

- We would like to hear about your bugs, feature requests, questions or quick feedback.
  Please search for the `existing issues <https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/issues>`_ before opening a new one. It would also be helpful
  if you follow the templates for issue and pull request creation. Please follow the `contributing guidelines <../CONTRIBUTING.rst>`_!!
- Request and vote for `Alexa features <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`_!
