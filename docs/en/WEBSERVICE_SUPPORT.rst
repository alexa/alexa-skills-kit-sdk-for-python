====================================
Host a Custom Skill as a Web Service
====================================

You can build a custom skill for Alexa by implementing a web service that
accepts requests from and sends responses to the Alexa service in the cloud.

The web service must meet certain requirements to handle requests sent by Alexa
and adhere to the Alexa Skills Kit interface standards. For more information,
see
`Host a Custom Skill as a Web Service <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html>`__
in the Alexa Skills Kit technical documentation.

.. warning::

    These features are currently in beta. You can view the source
    code in the
    `Ask Python Sdk <https://github.com/alexa/alexa-skills-kit-sdk-for-python>`__
    repo on GitHub. The interface might change when the features are released as
    stable.

ASD SDK Web Service Support
---------------------------

The Alexa Skills Kit SDK (ASK SDK) for Python provides boilerplate code for request
and timestamp verification through the
`ask-sdk-webservice-support <https://pypi.org/project/ask-sdk-webservice-support/>`__
package, which integrates with the `Skill Builder <SKILL_BUILDERS.html>`__
object. This package only provides the verification components and a base
handler to call the skill invocation, and is independent of the
underlying framework used for the web application development.

Installation
~~~~~~~~~~~~

You can install the ``ask-sdk-webservice-support`` package through `pip`.

.. important::

    The package has the `cryptography <https://cryptography.io/en/latest/>`__
    package as a dependency for request verification. The
    ``cryptography`` package might have additional prerequisites depending
    on the operating system. For more information, see the
    `installation instructions <https://cryptography.io/en/latest/installation/>`__
    in the ``cryptography`` documentation.


Generic Web Service Handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``WebserviceSkillHandler`` class registers the skill instance from
the ``SkillBuilder`` object, and provides a ``verify_request_and_dispatch``
method that verifies the input request before invoking the skill
handlers.

You can enable or disable request or timestamp
verification for testing purposes by setting the boolean parameters
``verify_signature`` and ``verify_timestamp`` on the
``WebserviceSkillHandler`` instance. You can also provide additional custom
verifiers that need to be applied on the input request before skill invocation.

The ``verify_request_and_dispatch`` method takes the ``http_headers``
and ``http_body`` from the web service, and returns the ``response`` in
string format, on successful skill invocation. You have to
convert the input and output into the web service-specific request and
response structures.

Usage
~~~~~

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder
    from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler

    skill_builder = SkillBuilder()

    # Implement request handlers, exception handlers, etc.
    # Register the handlers to the skill builder instance.

    webservice_handler = WebserviceSkillHandler(
        skill=skill_builder.create())

    # Convert the HTTP request headers and body into native format
    # of dict and str respectively, and call the dispatch method.
    response = webservice_handler.verify_request_and_dispatch(
        headers, body)

    # Convert the response str into web service format and return.


Framework-Specific Adapters
---------------------------

Flask and Django are two web service frameworks that are commonly
used to build web services in Python.
The ASK SDK provides framework-specific extensions to the
``ask-sdk-webservice-support`` package for both Flask and Django that
handle the request and response conversion internally. This
provides an easy way to integrate SDK skills that you've already developed to
make them work with your web service.

flask-ask-sdk Extension Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``flask-ask-sdk`` package provides a Flask extension that can
register a ``Flask`` application along with a custom skill. It also provides
helper methods to register the skill invocation as a URL endpoint to
the Flask application.

The ``flask-ask-sdk`` package follows the
`Flask extension structure <http://flask.pocoo.org/docs/1.0/extensiondev/#flask-extension-development>`__.
The ``SkillAdapter`` class constructor takes the following:

- A `skill` instance.
- A `skill id` to register the skill instance in the extension directory.
- An optional flask application, to register the extension in the application.

The class also provides an ``init_app`` method, to pass in the Flask
app instance later, to instantiate and configure the extension.

The request and timestamp verifications are enabled by default. You can use the app
configurations ``VERIFY_SIGNATURE_APP_CONFIG`` and
``VERIFY_TIMESTAMP_APP_CONFIG`` to disable or enable the
respective verifications by setting boolean values to them.

You can use the SkillAdapter's ``dispatch_request`` method to register
the skill as an endpoint url-rule. It handles the request and response
conversion, request and timestamp verification, and skill invocation.

Installation
````````````

You can install the ``flask-ask-sdk`` package through `pip`.

.. important::

    The package has the `cryptography <https://cryptography.io/en/latest/>`__
    package as a dependency for request verification. The
    ``cryptography`` package might have additional prerequisites depending
    on the operating system. For more information, see the
    `installation instructions <https://cryptography.io/en/latest/installation/>`__
    in the ``cryptography`` documentation.

Usage
`````

.. code-block:: python

    from flask import Flask
    from ask_sdk_core.skill_builder import SkillBuilder
    from flask_ask_sdk.skill_adapter import SkillAdapter

    app = Flask(__name__)
    skill_builder = SkillBuilder()
    # Register your intent handlers to the skill_builder object

    skill_adapter = SkillAdapter(
        skill=skill_builder.create(), skill_id=<SKILL_ID>, app=app)

    @app.route("/"):
    def invoke_skill:
        return skill_adapter.dispatch_request()

.. note::

    An instance of the extension is added to the application extensions
    mapping, using the key ``ASK_SDK_SKILL_ADAPTER``. Since multiple
    skills can be configured on different routes in the same application,
    through multiple extension instances, each extension is added as a
    skill ID mapping in the app extension's ``ASK_SDK_SKILL_ADAPTER``
    dictionary.

django-ask-sdk Extension Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``django-ask-sdk`` extension package provides a Django extension
that you can use to register a custom skill as an endpoint in the
Django application.

The extension provides a ``SkillAdapter`` view class. You
can instantiate the view class with a custom skill instance, built through
the ASK SDK Skill Builder object, and register it in the ``urls.py`` file
of the Django app so that the skill is invoked at the corresponding
endpoint.

The request and timestamp verifications are enabled by default. You can use
the constructor arguments ``verify_request`` and ``verify_timestamp``
to disable or enable the respective verifications by setting
boolean values to them.

Installation
````````````

You can install the ``django-ask-sdk`` extension through `pip`.

.. important::

    The package has the `cryptography <https://cryptography.io/en/latest/>`__
    package as a dependency for request verification. The
    ``cryptography`` package might have additional prerequisites depending
    on the operating system. For more information, see the
    `installation instructions <https://cryptography.io/en/latest/installation/>`__
    in the ``cryptography`` documentation.

.. note::

    The ``django-ask-sdk`` package is compatible with Python 3.0 or higher
    because it depends on Django 2.0 which only supports Python 3.

Usage
`````

If you develop a skill using the ``SkillBuilder`` instance,
then you can use the following in ``example.urls.py``
to register it as an endpoint in a Django app called ``example``:

.. code-block:: python

    import skill
    from django_ask_sdk.skill_adapter import SkillAdapter

    view = SkillAdapter.as_view(skill=skill.sb.create())

    urlpatterns = [
        path("/myskill", view, name='index')
    ]
