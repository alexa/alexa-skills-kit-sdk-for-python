=================
Skill Attributes
=================

This guide provides information on different scopes of attributes available
to the skill developer, and how to use them in the skill.

Attributes
==========

The SDK allows you to store and retrieve attributes at different scopes.
For example, attributes can be used to store data that you retrieve
on subsequent requests. You can also use attributes in your handler’s
``can_handle`` logic to add conditions during request routing.

An attribute consists of a key and a value. The key is enforced as a
``str`` type and the value is an unbounded ``object``. For session
and persistent attributes, you must ensure that value types are
serializable so they can be properly stored for subsequent retrieval.
This restriction does not apply to request-level attributes because they
do not persist outside of the request processing lifecycle.

Attribute Scopes
=================

Request Attributes
~~~~~~~~~~~~~~~~~~

Request attributes only last within a single request processing
lifecycle. Request attributes are initially empty when a request comes
in, and are discarded once a response has been produced.

Request attributes are useful with request and response interceptors.
For example, you can inject additional data and helper methods into
request attributes through a request interceptor so they are retrievable
by request handlers.

Session Attributes
~~~~~~~~~~~~~~~~~~

Session attributes persist throughout the lifespan of the current skill
session. Session attributes are available for use with any in-session
request. Any attributes set during the request processing lifecycle are
sent back to the Alexa service and provided in the next request in the
same session.

Session attributes do not require the use of an external storage
solution. They are not available for use when handling out-of-session
requests. They are discarded once the skill session closes.

.. note::

    Since session attributes are stored in the ``session`` property of
    Alexa's :py:class:`ask_sdk_model.request_envelope.RequestEnvelope`
    and :py:class:`ask_sdk_model.response_envelope.ResponseEnvelope`
    objects, only serializable types can be stored under them. The
    :py:class:`ask_sdk_core.serialize.DefaultSerializer` is used to
    serialize / deserialize the values.

Persistent Attributes
~~~~~~~~~~~~~~~~~~~~~

Persistent attributes persist beyond the lifecycle of the current
session. How these attributes are stored, including key scope (user ID
or device ID), TTL, and storage layer depends on the configuration of
the skill.

.. note::

    Persistent attributes are only available when you
    `configure the skill instance <SKILL_BUILDERS.html#skill-builders>`_
    with a ``PersistenceAdapter``. A call to the ``AttributesManager`` to
    retrieve or save persistent attributes will raise an exception if the
    ``PersistenceAdapter`` has not been configured.


AttributesManager
=================

The ``AttributesManager`` exposes attributes that you can retrieve and
update in your handlers. ``AttributesManager`` is available to handlers
via the `Handler Input <REQUEST_PROCESSING.html#handler-input>`_ object.
The ``AttributesManager`` takes care of attributes retrieval and saving
so that you can interact directly with attributes needed by your skill.

Interface
~~~~~~~~~

.. code:: python

    class AttributesManager(object):
        def __init__(self, request_envelope, persistence_adapter=None):
            # type: (RequestEnvelope, AbstractPersistenceAdapter) -> None
            ....

        @property
        def request_attributes(self):
            # type: () -> Dict[str, Any]
            # Request Attributes getter
            ....

        @request_attributes.setter
        def request_attributes(self, attributes):
            # type: (Dict[str, Any]) -> None
            # Request Attributes setter
            ....

        @property
        def session_attributes(self):
            # type: () -> Dict[str, Any]
            # Session Attributes getter
            ....

        @session_attributes.setter
        def session_attributes(self, attributes):
            # type: (Dict[str, Any]) -> None
            # Session Attributes setter
            ....

        @property
        def persistent_attributes(self):
            # type: () -> Dict[str, Any]
            # Persistence Attributes getter
            # Uses the Persistence adapter to get the attributes
            ....

        @persistent_attributes.setter
        def persistent_attributes(self, attributes):
            # type: (Dict[str, Any]) -> None
            # Persistent Attributes setter
            ....

        def save_persistent_attributes(self):
            # type: () -> None
            # Save the persistence attributes to the persistence layer
            ....

        def delete_persistent_attributes(self):
            # type: () -> None
            # Delete the persistence attributes from the persistence layer
            ....


The following example shows how you can retrieve and save persistent
attributes.

.. code:: python

    class PersistenceAttributesHandler(AbstractRequestHandler):
        def can_handle(handler_input):
            persistence_attr = handler_input.attributes_manager.persistent_attributes
            return persistence_attr['foo'] == 'bar'

        def handle(handler_input):
            persistence_attr = handler_input.attributes_manager.persistent_attributes
            persistence_attr['foo'] = 'baz'
            handler_input.attributes_manager.save_persistent_attributes()
            return handler_input.response_builder.response


.. note::

    To improve skill performance, ``AttributesManager`` caches the persistent
    attributes locally. ``persistent_attributes`` setter will only update the
    locally cached persistent attributes. You need to call
    ``save_persistent_attributes()`` to save persistent attributes to the
    persistence layer.

.. note::

    The ``delete_attributes`` on the default ``DynamoDbPersistenceAdapter``
    implementation will delete the persistence attributes from local cache
    as well as from the persistence layer (DynamoDb table).


PersistenceAdapter
==================

The ``AbstractPersistenceAdapter`` is used by ``AttributesManager`` when
retrieving and saving attributes to persistence layer (i.e. database or
local file system). You can register any customized ``PersistenceAdapter``
that conforms to the ``AbstractPersistenceAdapter`` interface with the SDK.

All implementations of ``AbstractPersistenceAdapter`` needs to follow
the following interface.

Interface
~~~~~~~~~

.. code:: python

    class AbstractPersistenceAdapter(object):
        def get_attributes(self, request_envelope):
            # type: (RequestEnvelope) -> Dict[str, Any]
            pass

        def save_attributes(self, request_envelope, attributes):
            # type: (RequestEnvelope, Dict[str, Any]) -> None
            pass


DynamoDbPersistenceAdapter
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``ask-sdk-dynamodb-persistence-adapter`` package
provides an implementation of ``AbstractPersistenceAdapter`` using `AWS
DynamoDB <https://aws.amazon.com/dynamodb/>`_.

Interface
---------

.. code:: python

    from ask_sdk_dynamodb.adapter import DynamoDbAdapter

    adapter = DynamoDbAdapter(table_name, partition_key_name="id",
                attribute_name="attributes", create_table=False,
                partition_keygen=user_id_partition_keygen,
                dynamodb_resource=boto3.resource("dynamodb")

Configuration Options
---------------------

    * **table_name** (string) - The name of the DynamoDB table used.

    * **partition_key_name** (string) - Optional. The name of the partition key column. Default to ``"id"`` if not provided.

    * **attributes_name** (string) - Optional. The name of the attributes column. Default to ``"attributes"`` if not provided.

    * **create_table** (boolean) - Optional. Set to ``True`` to have ``DynamoDbAdapter`` automatically create the table if it does not exist. Default to ``False`` if not provided.

    * **partition_keygen** (callable) - Optional. The function used to generate partition key using ``RequestEnvelope``. Default to generate the partition key using the ``user_id``.

    * **dynamodb_resource** (`AWS.DynamoDB ServiceResource <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource>`_ ) - Optional. The ``DynamoDBClient`` used to query AWS DynamoDB table. You can inject your ``DynamoDBClient`` with custom configuration here. Default to use ``boto3.resource("dynamodb")``.
