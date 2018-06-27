Skill Builders
==============

The SDK includes a ``SkillBuilder`` that provides utility methods, to
construct the ``Skill`` instance. It has the following structure:

.. code:: python

    class SkillBuilder(object):
        def __init__(self):
            # Initialize empty collections for request components,
            # exception handlers, interceptors.

        def add_request_handler(self, handler):
            # type: (AbstractRequestHandler) -> None
            ....

        def add_exception_handler(self, handler):
            # type: (AbstractExceptionHandler) -> None
            ....

        def add_global_request_interceptor(self, interceptor):
            # type: (AbstractRequestInterceptor) -> None
            ....

        def add_global_response_interceptor(self, interceptor):
            # type: (AbstractResponseInterceptor) -> None
            ....

        @property
        def skill_configuration(self):
            # type: () -> SkillConfiguration
            # Build configuration object using the registered components
            ....

        def create(self):
            # type: () -> Skill
            # Create the skill using the skill configuration
            ....

        def lambda_handler(self):
            # type: () -> LambdaHandler
            # Create a lambda handler function that can be tagged to
            # AWS Lambda handler.
            # Processes the alexa request before invoking the skill,
            # processes the alexa response before providing to the service
            ....

        def request_handler(self, can_handle_func):
            # type: (Callable[[HandlerInput], bool]) -> None
            # Request Handler decorator

        def exception_handler(self, can_handle_func):
            # type: (Callable[[HandlerInput, Exception], bool]) -> None
            # Exception Handler decorator

        def global_request_interceptor(self):
            # type: () -> None
            # Global Request Interceptor decorator

        def global_response_interceptor(self):
            # type: () -> None
            # Global Response Interceptor decorator

There are two extensions to ``SkillBuilder`` class, ``CustomSkillBuilder``
and ``StandardSkillBuilder``.

CustomSkillBuilder Class
------------------------

``CustomSkillBuilder`` is available in both ``ask-sdk-core`` and
``ask-sdk`` package. In addition to the common helper function above,
``CustomSkillBuilder`` also provides functions that allows you to
register custom ``AbstractPersistentAdapter`` and ``ApiClient``.

.. code:: python

    class CustomSkillBuilder(SkillBuilder):
        def __init__(self, persistence_adapter=None, api_client=None):
            # type: (AbstractPersistenceAdapter, ApiClient) -> None
            ....

        @property
        def skill_configuration(self):
            # Create skill configuration from skill builder along with
            # registered persistence adapter and api client
            ....


StandardSkillBuilder Class
--------------------------

``StandardSkillBuilder`` is available only in the ``ask-sdk`` package.
It uses ``DynamoDbPersistenceAdapter`` and ``DefaultApiClient`` to
provide Persistence and Service Client features. It also provides helper functions for
configuring the Dynamo DB table options.

.. code:: python

    class StandardSkillBuilder(SkillBuilder):
        def __init__(self,
                table_name=None, auto_create_table=None,
                partition_keygen=None, dynamodb_client=None):
            # type: (str, bool, Callable[[RequestEnvelope], str], ServiceResource) -> None)
            ....

        @property
        def skill_configuration(self):
            # Create skill configuration from skill builder along with
            # default api client and dynamodb persistence adapter with
            # the passed in table configuration options.
            ....

