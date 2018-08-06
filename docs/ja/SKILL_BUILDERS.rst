スキルビルダー
============

SDKには、``Skill`` インスタンスを作成する ``SkillBuilder`` が含まれています。構造は次のとおりです。

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

``SkillBuilder`` クラスには2つの拡張機能 ``CustomSkillBuilder`` および ``StandardSkillBuilder`` があります。

CustomSkillBuilderクラス
-----------------------

``CustomSkillBuilder`` は、``ask-sdk-core`` と ``ask-sdk`` パッケージの両方で使用できます。上の共通のヘルパー関数に加えて、``CustomSkillBuilder`` にも ``AbstractPersistentAdapter`` と ``ask_sdk_model.services.ApiClient`` クラスのカスタム実装を登録できる関数があります。

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


StandardSkillBuilderクラス
-------------------------

``StandardSkillBuilder`` は ``ask-sdk`` パッケージでのみ使用できます。これはpersistence_adapterを ``ask_sdk_dynamo.adapter.DynamoDbPersistenceAdapter`` として、api_clientを ``ask_sdk_core.api_client.DefaultApiClient`` として使用し、持続性機能およびサービスクライアント機能を提供する ``CustomSKillBuilder`` のラッパーです。また、Dynamo DBテーブルオプションを設定するオプションのパラメーターも提供します。

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

