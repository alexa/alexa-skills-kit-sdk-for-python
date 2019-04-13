Alexa Out-Of-Session Service Clients
====================================

Some of the Alexa Skills Kit Service APIs can also be used outside your
skill logic. For example, you can use Skill Messaging API to send
messages to a skill. The skill should be configured to handle the
events that are sent through these out-of-session service requests.

Since these service calls are `out-of-session` of a customer's skill
context, you need to provide an access token that has proper
service-dependant scope. So, to perform this service call **without using SDK**,
you would need to do the following :

* Obtain the required access token from Alexa, by retrieving the
  `ClientId` and `ClientSecret` from skill's permissions tab in developer
  console & calling the Alexa endpoint with proper scope.
* Call the service api with appropriate input parameters, along with
  authorized access token.

However, SDK provides service clients that short-circuits both steps
into a single service call. The client takes in your `ClientId` and
`ClientSecret`, injects the required scope w.r.t the service, retrieves
an access token, and uses it to call the Alexa service and provides
the end response object. This reduces the boiler plate code you need to
set-up, just to get the service call to be running.

.. important::

    The `ClientId` and `ClientSecret` values on the developer console
    are only shown for skills with appropriate permissions set. You can
    retrieve them from the skill -> permissions tab in developer console.

.. note::

    Since these service clients are out of context of a skill session,
    these are not available under ``service_client_factory`` in the
    ``handler_input`` object. The
    `In-Session Service Clients <SERVICE_CLIENTS.html>`__ document can
    provide more information on which services can be called in skill
    session context.

Available service clients
-------------------------

- **Proactive Events**: :py:class:`ask_sdk_model.services.proactive_events.proactive_events_service_client.ProactiveEventsServiceClient`

- **Skill Messaging**: :py:class:`ask_sdk_model.services.skill_messaging.skill_messaging_service_client.SkillMessagingServiceClient`

The service clients needs instances of
:py:class:`ask_sdk_model.services.api_configuration.ApiConfiguration` and
:py:class:`ask_sdk_model.services.authentication_configuration.AuthenticationConfiguration`
in the constructor.

AuthenticationConfiguration
---------------------------

The :py:class:`ask_sdk_model.services.authentication_configuration.AuthenticationConfiguration`
is the configuration class that accepts the `ClientId` and `ClientSecret` for
retrieving the access token from Alexa.

ApiConfiguration
----------------

The :py:class:`ask_sdk_model.services.api_configuration.ApiConfiguration` is
required for configuring the ``api_client`` to be used for making the service
calls, the ``serializer`` to use for serialization/deserialization of the
request/response objects, the ``api_endpoint`` to which the calls have to
be made.

.. note::

    The ``authorization_value`` on the ``ApiConfiguration`` class is
    not required for out-of-session calls.

.. note::

    Any customized Api Client can be provided, as long as it follows the
    :py:class:`ask_sdk_model.services.api_client.ApiClient` interface. A
    :py:class:`ask_sdk_core.api_client.DefaultApiClient` is available
    in the SDK for this usage.

.. note::

    Any customized Serializer can be provided, as long as it follows the
    :py:class:`ask_sdk_model.services.serializer.Serializer` interface.
    A :py:class:`ask_sdk_core.serialize.DefaultSerializer` implementation
    is available in the SDK for this usage.

ProactiveEventsServiceClient
----------------------------

The `Proactive Events API <https://developer.amazon.com/docs/smapi/proactive-events-api.html>`__
enables Alexa Skill Developers to send events to Alexa, which represent
factual data that may interest a customer. Upon receiving an event, Alexa
proactively delivers the information to customers subscribed to receive
these events.

This API currently supports one proactive channel, Alexa Notifications.
As more proactive channels are added in the future, developers will be
able to take advantage of them without requiring integration with a new
API.

Interface
~~~~~~~~~

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

More information on the models can be found `here <models/ask_sdk_model.services.proactive_events.html>`__.

Code-Sample
~~~~~~~~~~~

The following example shows how to send a sample weather proactive event to
Alexa, which will multicast it to all users registered on the skill to receive
it.

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

The `Skill Messaging API <https://developer.amazon.com/docs/smapi/skill-messaging-api-reference.html>`__
can be used to send a message request to a skill for a specified user.

Interface
~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.skill_messaging.SkillMessagingServiceClient:
        def __init__(self, api_configuration, authentication_configuration):
            # type: (ApiConfiguration, AuthenticationConfiguration) -> None

        def send_skill_message(self, user_id, send_skill_messaging_request):
            # type: (str, SendSkillMessagingRequest) -> Union[Error]

    class ask_sdk_model.services.skill_messaging.SkillMessagingRequest:
        def __init__(self, data=None, expires_after_seconds=None):
            # type: (Optional[object], Optional[int]) -> None

More information on the models can be found `here <models/ask_sdk_model.services.skill_messaging.html>`__.

Code-Sample
~~~~~~~~~~~

The following example shows a sample skill message sent to a skill, that
handles reminders (by having a handler that can handle requests of type
``Messaging.MessageReceived``.

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
----------------

The ``LwaClient`` is used by other `out-of-session` service clients,
to obtain the access token from Alexa, with the required scope specific to the
service. However, provided a specific scope, it can also be used natively
by the skill developers, to obtain access tokens.

Interface
~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.lwa.LwaClient:
        def __init__(self, api_configuration, authentication_configuration):
            # type: (ApiConfiguration, AuthenticationConfiguration) -> None

        def get_access_token_for_scope(self, scope):
            # type: (str) -> str

More information on the models can be found `here <models/ask_sdk_model.services.lwa.html>`__.

Code-Sample
~~~~~~~~~~~

The following example shows how to obtain an access-token for a scope `alexa:abc`.

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

