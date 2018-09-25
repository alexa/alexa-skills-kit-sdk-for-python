
Models
======

The SDK works on model classes rather than native Alexa JSON requests and
responses. These model classes are generated using the Request, Response JSON
schemas from the `developer docs <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html>`__. The source code for the model classes can be
found `here <https://github.com/alexa/alexa-apis-for-python>`__.

Subpackages
~~~~~~~~~~~

.. toctree::
  :maxdepth: 1

  ask_sdk_model.dialog
  ask_sdk_model.events
  ask_sdk_model.interfaces
  ask_sdk_model.services
  ask_sdk_model.slu
  ask_sdk_model.ui

Submodules
~~~~~~~~~~

.. note::

    Canonical imports have been added in the ``__init__.py`` of the package.
    This helps in importing the class directly from the package, than
    through the module.

    For eg: if ``package a`` has ``module b`` with
    ``class C``, you can do ``from a import C`` instead of
    ``from a.b import C``.

ask\_sdk\_model.application module
----------------------------------

.. automodule:: ask_sdk_model.application
    :members:
    :show-inheritance:

ask\_sdk\_model.context module
------------------------------

.. automodule:: ask_sdk_model.context
    :members:
    :show-inheritance:

ask\_sdk\_model.device module
-----------------------------

.. automodule:: ask_sdk_model.device
    :members:
    :show-inheritance:

ask\_sdk\_model.dialog\_state module
------------------------------------

.. automodule:: ask_sdk_model.dialog_state
    :members:
    :show-inheritance:

ask\_sdk\_model.directive module
--------------------------------

.. automodule:: ask_sdk_model.directive
    :members:
    :show-inheritance:

ask\_sdk\_model.intent module
-----------------------------

.. automodule:: ask_sdk_model.intent
    :members:
    :show-inheritance:

ask\_sdk\_model.intent\_confirmation\_status module
---------------------------------------------------

.. automodule:: ask_sdk_model.intent_confirmation_status
    :members:
    :show-inheritance:

ask\_sdk\_model.intent\_request module
--------------------------------------

.. automodule:: ask_sdk_model.intent_request
    :members:
    :show-inheritance:

ask\_sdk\_model.launch\_request module
--------------------------------------

.. automodule:: ask_sdk_model.launch_request
    :members:
    :show-inheritance:

ask\_sdk\_model.permissions module
----------------------------------

.. automodule:: ask_sdk_model.permissions
    :members:
    :show-inheritance:

ask\_sdk\_model.request module
------------------------------

.. automodule:: ask_sdk_model.request
    :members:
    :show-inheritance:

ask\_sdk\_model.request\_envelope module
----------------------------------------

.. automodule:: ask_sdk_model.request_envelope
    :members:
    :show-inheritance:

ask\_sdk\_model.response module
-------------------------------

.. automodule:: ask_sdk_model.response
    :members:
    :show-inheritance:

ask\_sdk\_model.response\_envelope module
-----------------------------------------

.. automodule:: ask_sdk_model.response_envelope
    :members:
    :show-inheritance:

ask\_sdk\_model.session module
------------------------------

.. automodule:: ask_sdk_model.session
    :members:
    :show-inheritance:

ask\_sdk\_model.session\_ended\_error module
--------------------------------------------

.. automodule:: ask_sdk_model.session_ended_error
    :members:
    :show-inheritance:

ask\_sdk\_model.session\_ended\_error\_type module
--------------------------------------------------

.. automodule:: ask_sdk_model.session_ended_error_type
    :members:
    :show-inheritance:

ask\_sdk\_model.session\_ended\_reason module
---------------------------------------------

.. automodule:: ask_sdk_model.session_ended_reason
    :members:
    :show-inheritance:

ask\_sdk\_model.session\_ended\_request module
----------------------------------------------

.. automodule:: ask_sdk_model.session_ended_request
    :members:
    :show-inheritance:

ask\_sdk\_model.slot module
---------------------------

.. automodule:: ask_sdk_model.slot
    :members:
    :show-inheritance:

ask\_sdk\_model.slot\_confirmation\_status module
-------------------------------------------------

.. automodule:: ask_sdk_model.slot_confirmation_status
    :members:
    :show-inheritance:

ask\_sdk\_model.supported\_interfaces module
--------------------------------------------

.. automodule:: ask_sdk_model.supported_interfaces
    :members:
    :show-inheritance:

ask\_sdk\_model.user module
---------------------------

.. automodule:: ask_sdk_model.user
    :members:
    :show-inheritance:

ask\_sdk\_model.permission_status module
---------------------------

.. automodule:: ask_sdk_model.permission_status
    :members:
    :show-inheritance:

ask\_sdk\_model.scope module
---------------------------

.. automodule:: ask_sdk_model.scope
    :members:
    :show-inheritance:
