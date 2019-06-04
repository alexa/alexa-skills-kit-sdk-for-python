======================
Alexaセッション外サービスクライアント
======================

一部のAlexa Skills
KitサービスAPIは、スキルのロジックの外で使用することもできます。たとえば、スキルメッセージAPIを使って、スキルにメッセージを送信できます。こうしたセッション外のサービスリクエストを通じて送信されるイベントを処理できるよう、スキルを設定してください。

この場合、サービスの呼び出しはユーザーのスキルコンテキストのセッション外で行われるため、スコープがサービスに依存するよう正しく設定されたアクセストークンを指定する必要があります。そのため、\ **SDKを使わずに**\ サービスを呼び出すには、以下の手順を実行します。

-  開発者コンソールでスキル＞アクセス権限タブからクライアントIDとクライアントシークレットを取得し、正しいスコープを指定してAlexaエンドポイントを呼び出し、Alexaから必要なアクセストークンを取得します。

-  適切な入力パラメーターと認可済みのアクセストークンを指定して、サービスAPIを呼び出します。

SDKには、この両方の手順が1回のサービス呼び出しで行われるサービスクライアントが用意されています。クライアントは、クライアントIDとクライアントシークレットを受け取り、サービスに関する必要なスコープを設定してアクセストークンを取得し、そのトークンを使ってAlexaサービスを呼び出して、目的の応答オブジェクトを提供します。これによって、サービスを呼び出すためだけにボイラープレートコード（毎回書かなければならないお決まりのコード）を設定する手間をが省略できます。

.. important::

    開発者コンソールでは、適切な権限が設定されているスキルにのみ、クライアントIDとクライアントシークレットの値が表示されます。これらの値は、開発者コンソールのスキル＞アクセス権限タブから取得できます。

.. note::

    このようなサービスクライアントはスキルセッションのコンテキスト外であるため、handler_inputオブジェクトの``service_client_factory``では使用できません。スキルセッションのコンテキストで呼び出せるサービスの詳細については、 `In-Session Service Clients（英語） <SERVICE_CLIENTS.html>`__ を参照してください。

利用可能なサービスクライアント
-------------------

-  **プロアクティブイベント**\ : :py:class:`ask_sdk_model.services.proactive_events.proactive_events_service_client.ProactiveEventsServiceClient`

-  **スキルメッセージ**\ ： :py:class:`ask_sdk_model.services.skill_messaging.skill_messaging_service_client.SkillMessagingServiceClient`

サービスクライアントのコンストラクターには :py:class:`ask_sdk_model.services.api_configuration.ApiConfiguration` と :py:class:`ask_sdk_model.services.authentication_configuration.AuthenticationConfiguration` のインスタンスが必要です。

AuthenticationConfiguration
---------------------------

:py:class:`ask_sdk_model.services.authentication_configuration.AuthenticationConfiguration` はコンフィギュレーションクラスであり、Alexaからアクセストークンを取得するためにクライアントIDとクライアントシークレットを受け取ります。

ApiConfiguration
----------------

:py:class:`ask_sdk_model.services.api_configuration.ApiConfiguration` は、api_client（サービスを呼び出すために使用）、serializer（リクエスト／応答オブジェクトのシリアル化／逆シリアル化に使用）、api_endpoint（呼び出し先）の設定に必要です。

.. note::

    セッション外の呼び出しには、ApiConfigurationクラスのauthorization_valueは不要です。

.. note::

    カスタマイズされたAPIクライアントは、:py:class:`ask_sdk_model.services.api_client.ApiClient`  インターフェースに従っていれば指定できます。この方法で使用する場合、SDKの\ :py:class:`ask_sdk_core.api_client.DefaultApiClient` を利用できます。

.. note::

    カスタマイズされたシリアライザーは、:py:class:`ask_sdk_model.services.serializer.Serializer`  インターフェースに従っていれば指定できます。この方法で使用する場合、SDKの :py:class:`ask_sdk_core.serialize.DefaultSerializer`  実装を利用できます。

ProactiveEventsServiceClient
----------------------------

`プロアクティブイベントAPI <https://developer.amazon.com/docs/smapi/proactive-events-api.html>`__ を使用すると、Alexaスキル開発者はAlexaにイベントを送信できます。イベントとは、ユーザーが興味を持つと考えられる事実に基づくデータのことです。イベントを受信すると、Alexaは、これらのイベントを受け取るようサブスクリプションを行ったユーザーに、プロアクティブに情報を配信します。

現在、このAPIは、Alexa通知というプロアクティブチャネルを1つサポートしています。将来的にプロアクティブチャネルが追加されると、開発者は新しいAPIを統合しなくても、追加のチャネルを利用できるようになります。

インターフェース
~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.proactive_events.ProactiveEventsServiceClient:
        def __init__(self, api_configuration, authentication_configuration):
            # type: (ApiConfiguration, AuthenticationConfiguration) -> None

        def create_proactive_event(self, create_proactive_event_request, stage):
            # type: (CreateProactiveEventRequest, SkillStage) -> Union[Error]

    class ask_sdk_model.services.proactive_events.CreateProactiveEventRequest:
        def __init__(self, timestamp=None, reference_id=None, expiry_time=None, event=None, localized_attributes=None, relevant_audience=None):
            # type: (Optional[datetime], Optional[str], Optional[datetime], Optional[Event], Optional[List[object]], Optional[RelevantAudience]) -> None

    class ask_sdk_model.services.proactive_events.SkillStage(Enum):
        DEVELOPMENT = "DEVELOPMENT"
        LIVE = "LIVE"

    class ask_sdk_model.services.proactive_events.Event:
        def __init__(self, name=None, payload=None):
            # type: (Optional[str], Optional[object]) -> None

    class ask_sdk_model.services.proactive_events.RelevantAudience:
        def __init__(self, object_type=None, payload=None):
            # type: (Optional[RelevantAudienceType], Optional[object]) -> None

    class ask_sdk_model.services.proactive_events.RelevantAudienceType(Enum):
        Unicast = "Unicast"
        Multicast = "Multicast"

モデルの詳細については `こちら <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/docs/en/models/ask_sdk_model.services.proactive_events.html>`__ を参照してください。

サンプルコード
~~~~~~~

以下の例で、天気のプロアクティブイベントをAlexaに送信する方法を示します。Alexaは受信したイベントを、スキルに登録されているすべてのユーザーにマルチキャストします。

.. code-block:: python

    from datetime import datetime, timedelta

    from ask_sdk_model.services.proactive_events import (
        ProactiveEventsServiceClient, CreateProactiveEventRequest,
        RelevantAudienceType, RelevantAudience, SkillStage, Event)
    from ask_sdk_model.services import (
        ApiConfiguration, AuthenticationConfiguration)
    from ask_sdk_core.serialize import DefaultSerializer
    from ask_sdk_core.api_client import DefaultApiClient


    def create_notification():
        client_id = "XXXX"
        client_secret = "XXXX"
        user_id = "XXXX"

        proactive_client = ProactiveEventsServiceClient(
            api_configuration=ApiConfiguration(
                serializer=DefaultSerializer(),
                api_client=DefaultApiClient(),
                api_endpoint="https://api.amazonalexa.com"),
            authentication_configuration=AuthenticationConfiguration(
                client_id=client_id,
                client_secret=client_secret))

        weather_event = Event(
            name="AMAZON.WeatherAlert.Activated",
            payload={
                "weatherAlert": {
                    "alertType": "SNOW_STORM",
                    "source": "localizedattribute:source"
                }
            }
        )

        create_event = CreateProactiveEventRequest(
            timestamp=datetime.utcnow(),
            reference_id="1234",
            expiry_time=datetime.utcnow() + timedelta(hours=1),
            event=weather_event,
            localized_attributes=[{"locale": "en-US", "source": "Foo"}],
            relevant_audience=RelevantAudience(
                object_type=RelevantAudienceType.Multicast,
                payload={}
            )
        )

        proactive_client.create_proactive_event(
            create_proactive_event_request=create_event,
            stage=SkillStage.DEVELOPMENT)

SkillMessagingServiceClient
---------------------------

指定されたユーザーのスキルにメッセージリクエストを送信するには `スキルメッセージAPI <https://developer.amazon.com/docs/smapi/skill-messaging-api-reference.html>`__ を使います。

インターフェース
~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.skill_messaging.SkillMessagingServiceClient:
        def __init__(self, api_configuration, authentication_configuration):
            # type: (ApiConfiguration, AuthenticationConfiguration) -> None

        def send_skill_message(self, user_id, send_skill_messaging_request):
            # type: (str, SendSkillMessagingRequest) -> Union[Error]

    class ask_sdk_model.services.skill_messaging.SkillMessagingRequest:
        def __init__(self, data=None, expires_after_seconds=None):
            # type: (Optional[object], Optional[int]) -> None

モデルの詳細については、 `こちら <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/docs/en/models/ask_sdk_model.services.skill_messaging.html>`__ を参照してください。

サンプルコード
~~~~~~~

以下に、スキルメッセージをスキルに送信する例を示します。スキルは、``Messaging.MessageReceived``型のリクエストを処理できるハンドラーにより、リマインダーを処理します。

.. code-block:: python

    from ask_sdk_core.api_client import DefaultApiClient
    from ask_sdk_model.services import (
        ApiConfiguration, AuthenticationConfiguration)
    from ask_sdk_core.serialize import DefaultSerializer
    from ask_sdk_model.services.skill_messaging import (
        SkillMessagingServiceClient, SendSkillMessagingRequest)


    def send_skill_messaging():
        reminder_id = "XXXX"
        client_id = "XXXX"
        client_secret = "XXXX"
        user_id = "XXXX"

        skill_messaging_client = SkillMessagingServiceClient(
            api_configuration=ApiConfiguration(
                serializer=DefaultSerializer(),
                api_client=DefaultApiClient(),
                api_endpoint="https://api.amazonalexa.com"),
            authentication_configuration=AuthenticationConfiguration(
                client_id=client_id,
                client_secret=client_secret)
        )

        message = SendSkillMessagingRequest(
            data={"reminder_id": reminder_id})

        skill_messaging_client.send_skill_message(
            user_id=user_id, send_skill_messaging_request=message)

LwaClient
---------

``LwaClient``は、他のセッション外サービスクライアントが、サービスに固有の必要なスコープを設定してAlexaからアクセストークンを取得するために使用します。ただし、特定のスコープを指定すれば、スキル開発者がアクセストークンを取得するためにネイティブに使用することもできます。

インターフェース
~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.lwa.LwaClient:
        def __init__(self, api_configuration, authentication_configuration):
            # type: (ApiConfiguration, AuthenticationConfiguration) -> None

        def get_access_token_for_scope(self, scope):
            # type: (str) -> str

モデルの詳細については、 `こちら <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/docs/en/models/ask_sdk_model.services.lwa.html>`__ を参照してください。

サンプルコード
~~~~~~~

以下に、``alexa:abc``スコープのアクセストークンを取得する方法の例を示します。

.. code-block:: python

    from ask_sdk_core.api_client import DefaultApiClient
    from ask_sdk_model.services import (
        ApiConfiguration, AuthenticationConfiguration)
    from ask_sdk_core.serialize import DefaultSerializer
    from ask_sdk_model.services.lwa import LwaClient

    def out_of_session_reminder_update():
        client_id = "XXXX"
        client_secret = "XXXX"
        scope = "alexa:abc"

        api_configuration = ApiConfiguration(
                serializer=DefaultSerializer(),
                api_client=DefaultApiClient(),
                api_endpoint="https://api.amazonalexa.com")

        lwa_client = LwaClient(
            api_configuration=api_configuration,
            authentication_configuration=AuthenticationConfiguration(
                client_id=client_id,
                client_secret=client_secret))

        access_token = lwa_client.get_access_token_for_scope(scope=scope)
