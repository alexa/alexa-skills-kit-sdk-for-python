Alexaサービスクライアント
======================

Alexa Skills Kitは複数のサービスAPIを提供しています。
あなたのスキル経験をパーソナライズする。 SDKには以下のサービスクライアントが含まれています。
スキルロジック内からAlexa APIを呼び出すために使用できます。

.. note::

    SDKは、セッション外のAlexa APIのサポートも提供します。
    （ `プロアクティブイベント<https://developer.amazon.com/docs/smapi/proactive-events-api.html>` __、
    `スキルメッセージング<https://developer.amazon.com/docs/smapi/send-a-message-request-to-a-skill.html>` __
    等。）。 SDKを介してこれらのサービスを呼び出す方法の詳細については、
    チェックしてください
    `セッション外のAlexaサービスクライアント<OUT_OF_SESSION_SERVICE_CLIENTS.html>` __。

ServiceClientFactory
--------------------

`Handler Input <REQUEST_PROCESSING.html＃handler-input>` _の中に含まれる `` service_client_factory``
サポートされているすべてのAlexaサービスのクライアントインスタンスを取得できます。それ
個々のサービスクライアントを作成し、メタデータを設定します。
`` api_access_token``や `` api_endpoint``のように。

`` service_client_factory``を通して `` handler_input``で利用可能ですので
属性、サービスクライアントは任意のリクエストハンドラで使用できます、例外
ハンドラー、および要求、応答のインターセプター。

利用可能なサービスクライアント
--------------------------

.. code-block:: python

    def get_device_address_service(self):
        # type: () -> ask_sdk_model.services.device_address.DeviceAddressServiceClient

    def get_directive_service(self):
        # type: () -> ask_sdk_model.services.directive.DirectiveServiceClient

    def get_list_management_service(self):
        # type: () -> ask_sdk_model.services.list_management.ListManagementServiceClient

    def get_monetization_service(self):
        # type: () -> ask_sdk_model.services.monetization.MonetizationServiceClient

    def get_ups_service(self):
        # type: () -> ask_sdk_model.services.ups.UpsServiceClient

    def get_reminder_management_service(self):
        # type: () -> ask_sdk_model.services.reminder_management.ReminderManagementServiceClient


.. note::

    `` service_client_factory``はあなたが利用できる場合にのみ利用可能です。
    `スキルインスタンスを設定する<SKILL_BUILDERS.html＃skill-builders>`_
    ApiClientを使って

.. note::

    さまざまなサービスクライアント用のインターフェースおよびコードサンプルの詳細については、`こちらを参照してください。<https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html#alexa-service-clients>`__

Apiクライアント
-------------

`` ask_sdk_model.services.api_client.ApiClient``は
AlexaサービスへのAPI呼び出しを行うときは `` service_client_factory``。
以下に準拠する任意のカスタマイズされた「ApiClient」を登録できます。
SDKとのインタフェース

インタフェース
~~~~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.api_client.ApiClient:
        def invoke(self, request):
            # type: (ApiClientRequest) -> ApiClientResponse

    class ask_sdk_model.services.api_client_request.ApiClientRequest(ApiClientMessage):
        def __init__(self, headers=None, body=None, url=None, method=None):
            # type: (List[Tuple[str, str]], str, str, str) -> None

    class ask_sdk_model.services.api_client_request.ApiClientResponse(ApiClientMessage):
        def __init__(self, headers=None, body=None, status_code=None):
            # type: (List[Tuple[str, str]], str, int) -> None

    class ask_sdk_model.services.api_client_message.ApiClientMessage(object):
        def __init__(self, headers=None, body=None):
            # type: (List[Tuple[str, str]], str) -> None

`CustomSkillBuilder <SKILL_BUILDERS.html＃customskillbuilder-class>` __
ApiClientを登録するためにコンストラクタを使用することができます。

.. code-block:: python

    from ask_sdk_core.skill_builder import CustomSkillBuilder

    sb = CustomSkillBuilder(api_client = <YourClassInstance>)

DefaultApiClient
~~~~~~~~~~~~~~~~

`` request``ライブラリに基づいた `` DefaultApiClient``は、以下で利用可能になります。
スキル開発者のための `` ask_sdk_core.api_client``モジュール

このクライアントはデフォルトで `StandardSkillBuilder <SKILL_BUILDERS.html＃standardskillbuilder-class>` __に登録されています。
あるいは、スキル開発者はこのクライアントをに登録することができます。
CustomSkillBuilderです。

.. code-block:: python

    from ask_sdk_core.skill_builder import CustomSkillBuilder
    from ask_sdk_core.api_client import DefaultApiClient

    sb = CustomSkillBuilder(api_client=DefaultApiClient())

