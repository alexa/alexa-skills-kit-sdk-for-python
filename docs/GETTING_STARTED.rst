=======================
Setting Up The ASK SDK
=======================

Introduction
------------

This guide describes how to install the ASK SDK for Python in preparation for
developing an Alexa skill.

Prerequisites
-------------

The ASK SDK for Python requires **Python 2 (>= 2.7)** or **Python 3 (>= 3.6)**.
Before continuing, make sure you have a supported version of Python installed.
To show the version, from a command prompt run the following command:

.. code-block:: sh

    >>> python --version
    Python 3.6.5

You can download the latest version of Python
`here <https://www.python.org/downloads/>`_.


Adding the ASK SDK for Python to Your Project
---------------------------------------------

You can download and install the ASK SDK for Python from the Python Package
Index (PyPI) using the command line tool pip. If you are using Python 2
version 2.7.9 or later or Python 3 version 3.4 or later, pip should be
installed with Python by default.

Many Python developers prefer to work in a virtual environment, which is an
isolated Python environment that helps manage project dependencies and package
versions. The easiest way to get started is to install the SDK in a virtual
environment. See the section
`Set up the SDK in a virtual environment <#set-up-the-sdk-in-a-virtual-environment>`_.

Another option is to install the ASK SDK for Python to a specific folder. This
ensures that you have the required dependencies and makes it easy to locate
and deploy the required files for your finished skill. See the section
`Set up the SDK in a specific folder <#set-up-the-sdk-in-a-specific-folder>`_.

Set up the SDK in a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following command to create a virtual environment and change to the
created folder:

.. code-block:: sh

    >>> virtualenv skill

Next, activate your virtual environment. If you are using MacOS or Linux,
use the following command:

.. code-block:: sh

    >>> source skill/bin/activate

Windows users need to use the following command:

.. code-block:: bat

    >>> skill\Script\activate

The command prompt should now be prefixed with (skill) indicating that you
are working inside the virtual environment. Use the following command to
install the ASK SDK for Python:

.. code-block:: sh

    >>> pip install ask-sdk

On MacOS and Linux, depending on the version of Python you are using, the
SDK will be installed into the ``skill/lib/Python3.6/site-packages`` folder.
On Windows it is installed to ``skill\Lib\site-packages``. The site-packages
folder is populated with directories including:

.. code-block:: sh

    ask_sdk
    ask_sdk_core
    ask_sdk_dynamodb
    ask_sdk_model
    boto3
    …

Set up the SDK in a specific folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get started, from a command prompt create a new folder for your Alexa skill
and navigate to the folder:

.. code-block:: sh

    >>> mkdir skill
    >>> cd skill

Next, install the ASK SDK for Python using pip. The ``-t`` option targets a
specific folder for installation:

.. code-block:: sh

    >>> pip install ask-sdk -t ask-sdk

This creates a folder named ask-sdk inside your skill folder and installs
the ASK SDK for Python and its dependencies. Your skill directory should now
contain the folder ask-sdk, which is populated with directories including:

.. code-block:: sh

    ask_sdk
    ask_sdk_core
    ask_sdk_dynamodb
    ask_sdk_model
    boto3
    …

Note
++++

If using Mac OS X and you have Python installed using
`Homebrew <http://brew.sh/>`_, the preceding command will not work. A simple
workaround is to add a ``setup.cfg`` file in your **ask-sdk** directory with
the following content:

.. code-block:: sh

    [install]
    prefix=

Navigate to the ask-sdk folder and run the pip install command:

.. code-block:: sh

    >>> cd ask-sdk
    >>> pip install ask-sdk -t .

More on this can be checked on the
`homebrew docs <https://github.com/Homebrew/brew/blob/master/docs/Homebrew-and-Python.md#setuptools-pip-etc>`_

Next Steps
----------

Now that you've added the SDK to your project, you're ready to begin
developing your skill. Proceed to the next section
`Developing Your First Skill <DEVELOPING_YOUR_FIRST_SKILL.rst>`_, for
instructions on getting started with a basic skill.
