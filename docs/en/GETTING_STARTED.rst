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

    $ python --version
    Python 3.6.5

You can download the latest version of Python
`here <https://www.python.org/downloads/>`_.


Adding the ASK SDK for Python to Your Project
---------------------------------------------

You can download and install the ASK SDK for Python from the Python Package
Index (PyPI) using the command line tool ``pip``. If you are using **Python 2
version 2.7.9 or later** or **Python 3 version 3.4 or later**, ``pip`` should be
installed with Python by default.

Many Python developers prefer to work in a virtual environment, which is an
isolated Python environment that helps manage project dependencies and package
versions. The easiest way to get started is to install the SDK in a virtual
environment. See the section
`Set up the SDK in a virtual environment <#option-1-set-up-the-sdk-in-a-virtual-environment>`_.

Another option is to install the ASK SDK for Python to a specific folder. This
ensures that you have the required dependencies and makes it easy to locate
and deploy the required files for your finished skill. See the section
`Set up the SDK in a specific folder <#option-2-set-up-the-sdk-in-a-specific-folder>`_.

.. tip::

    The following steps showcase the installation process for the standard SDK
    distribution. The standard SDK distribution ``ask-sdk`` is the easiest way to quickly
    get up and running with the SDK. It includes the core SDK package,
    the model package, and the package for the Amazon DynamoDB persistence
    adapter that enables storing skill attributes in DynamoDB.

    If you do not need everything in the standard distribution ``ask-sdk``,
    you can install the core package and expand with individual add-on packages
    later.

    For doing that, change the package name in the ``pip install <package name>``
    commands in the following sections with ``ask-sdk-core`` for the core
    package and ``ask-sdk-dynamodb-persistence-adapter`` for the DynamoDB
    persistence adapter add-on.

Option 1: Set up the SDK in a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This option requires you to install the ``virtualenv`` package. ``virtualenv``
is a tool to create isolated Python environments. To get started, from a
command prompt, use the following command to install the package:

.. code-block:: sh

    $ pip install virtualenv

Next, create a create a new folder for your Alexa skill and navigate to the folder:

.. code-block:: sh

    $ mkdir skill
    $ cd skill

Next, create a virtual environment called ``skill_env`` by issuing the
following command:

.. code-block:: sh

    $ virtualenv skill_env

Next, activate your virtual environment and install the sdk.

.. tabs::

    .. tab:: MacOS / Linux

        Run the following command to activate your virtual environment:

        .. code-block:: sh

            $ source skill_env/bin/activate

        The command prompt should now be prefixed with *(skill_env)*,
        indicating that you are working inside the virtual environment. Use
        the following command to install the ASK Python SDK:

        .. code-block:: sh

            (skill_env)$ pip install ask-sdk

        Depending on the version of Python you are using, the SDK will be
        installed into the ``skill_env/lib/Python3.6/site-packages`` folder.
        The site-packages folder is populated with directories including:

        .. code-block:: sh

            ask_sdk
            ask_sdk_core
            ask_sdk_dynamodb
            ask_sdk_model
            boto3
            …

    .. tab:: Windows

        Run the following command to activate your virtual environment:

        .. code-block:: bat

            $ skill_env\Scripts\activate

        The command prompt should now be prefixed with *(skill_env)*,
        indicating that you are working inside the virtual environment. Use
        the following command to install the ASK Python SDK:

        .. code-block:: bat

            (skill_env)$ pip install ask-sdk

        The SDK will be installed into the ``skill\Lib\site-packages`` folder.
        The site-packages folder is populated with directories including:

        .. code-block:: bat

            ask_sdk
            ask_sdk_core
            ask_sdk_dynamodb
            ask_sdk_model
            boto3
            …


Option 2: Set up the SDK in a specific folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get started, from a command prompt create a new folder for your Alexa skill
and navigate to the folder:

.. code-block:: sh

    $ mkdir skill
    $ cd skill

Next, install the ASK SDK for Python using pip. The ``-t`` option targets a
specific folder for installation:

.. code-block:: sh

    $ pip install ask-sdk -t skill_env

This creates a folder named ``skill_env`` inside your ``skill`` folder and installs
the ASK SDK for Python and its dependencies. Your ``skill`` directory should now
contain the folder ``skill_env``, which is populated with directories including:

.. code-block:: sh

    ask_sdk
    ask_sdk_core
    ask_sdk_dynamodb
    ask_sdk_model
    boto3
    …

.. note::

    If using Mac OS X and you have Python installed using
    `Homebrew <http://brew.sh/>`_, the preceding command will not work. A simple
    workaround is to add a ``setup.cfg`` file in your **ask-sdk** directory with
    the following content:

    .. code-block:: sh

        [install]
        prefix=

    Navigate to the skill_env folder and run the pip install command:

    .. code-block:: sh

        $ cd skill_env
        $ pip install ask-sdk -t .

    More on this can be checked on the
    `homebrew docs <https://github.com/Homebrew/brew/blob/master/docs/Homebrew-and-Python.md#setuptools-pip-etc>`_

Next Steps
----------

Now that you've added the SDK to your project, you're ready to begin
developing your skill. Proceed to the next section
`Developing Your First Skill <DEVELOPING_YOUR_FIRST_SKILL.html>`_, for
instructions on getting started with a basic skill.
