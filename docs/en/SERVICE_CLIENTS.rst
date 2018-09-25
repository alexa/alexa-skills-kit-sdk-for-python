Alexa Service Clients
=====================

Alexa Skills Kit provides multiple service APIs that you can use to
personalize your skill experience. The SDK includes service clients that
you can use to call Alexa APIs from within your skill logic.

ServiceClientFactory
--------------------

The ``service_client_factory`` contained inside the `Handler Input <REQUEST_PROCESSING.html#handler-input>`_
allows you to retrieve client instances for every supported Alexa service. It
takes care of creating individual service clients and configuring the metadata
like ``api_access_token`` and ``api_endpoint``.

Since it is available in ``handler_input`` through ``service_client_factory``
attribute, service clients can be used in any request handler, exception
handler, and request, response interceptors.

Available service clients
~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. note::

    The ``service_client_factory`` is only available for use, when you
    `configure the skill instance <SKILL_BUILDERS.html#skill-builders>`_
    with an ``ApiClient``.

ApiClient
---------

The ``ask_sdk_model.services.api_client.ApiClient`` is used by the
``service_client_factory`` when making API calls to Alexa services.
You can register any customized ``ApiClient`` that conforms to the following
interface with the SDK.

Interface
~~~~~~~~~

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

The `CustomSkillBuilder <SKILL_BUILDERS.html#customskillbuilder-class>`__
constructor can be used to register the ApiClient.

.. code-block:: python

    from ask_sdk_core.skill_builder import CustomSkillBuilder

    sb = CustomSkillBuilder(api_client=<YourClassInstance>)

DefaultApiClient
~~~~~~~~~~~~~~~~

A ``DefaultApiClient`` based on the ``requests`` library, is made available in
the ``ask_sdk_core.api_client`` module for skill developers.

This client is registered by default in the `StandardSkillBuilder <SKILL_BUILDERS.html#standardskillbuilder-class>`__.
Alternatively, skill developers can register this client to the
``CustomSkillBuilder``.

.. code-block:: python

    from ask_sdk_core.skill_builder import CustomSkillBuilder
    from ask_sdk_core.api_client import DefaultApiClient

    sb = CustomSkillBuilder(api_client=DefaultApiClient())

DeviceAddressServiceClient
--------------------------

``DeviceAddressServiceClient`` can be used to query `Device Address API <https://developer.amazon.com/docs/custom-skills/device-address-api.html>`_
for address data associated with the customer's Alexa device. You can then
use this address data to provide key functionality for the skill, or to
enhance the customer experience. For example, your skill could provide a list
of nearby store locations or provide restaurant recommendations using this
address information.

Interface
~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.device_address.DeviceAddressServiceClient:
        def get_country_and_postal_code(device_id):
            # type: (str) -> Union[ShortAddress, Error]

        def get_full_address(self, device_id):
            # type: (str) -> Union[Address, Error]

    class ask_sdk_model.services.device_address.ShortAddress:
        def __init__(self, country_code=None, postal_code=None):
            # type: (Optional[str], Optional[str]) -> None

    class ask_sdk_model.services.device_address.Address:
        def __init__(
            self, address_line1=None, address_line2=None, address_line3=None,
            country_code=None, state_or_region=None, city=None,
            district_or_county=None, postal_code=None):
            # type: (Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]) -> None

.. note::

    The device_id can be retrieved from ``handler_input.request_envelope.context.system.device.device_id``.

More information on the models can be found `here <models/ask_sdk_model.services.device_address.html>`__.

Code Sample
~~~~~~~~~~~

The following example shows how a request handler retrieves customer's full
address.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.utils import is_intent_name
    from ask_sdk_model.response import Response
    from ask_sdk_model.ui import AskForPermissionsConsentCard
    from ask_sdk_model.services import ServiceException

    NOTIFY_MISSING_PERMISSIONS = ("Please enable Location permissions in "
                                  "the Amazon Alexa app.")
    NO_ADDRESS = ("It looks like you don't have an address set. "
                  "You can set your address from the companion app.")
    ADDRESS_AVAILABLE = "Here is your full address: {}, {}, {}"
    ERROR = "Uh Oh. Looks like something went wrong."
    LOCATION_FAILURE = ("There was an error with the Device Address API. "
                        "Please try again.")

    permissions = ["read::alexa:device:all:address"]

    class GetAddressIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("GetAddressIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            req_envelope = handler_input.request_envelope
            service_client_fact = handler_input.service_client_factory
            response_builder = handler_input.response_builder

            if not (req_envelope.context.system.user.permissions and
                    req_envelope.context.system.user.permissions.consent_token):
                response_builder.speak(NOTIFY_MISSING_PERMISSIONS)
                response_builder.set_card(
                    AskForPermissionsConsentCard(permissions=permissions))
                return response_builder.response

            try:
                device_id = req_envelope.context.system.device.device_id
                device_addr_client = service_client_fact.get_device_address_service()
                addr = device_addr_client.get_full_address(device_id)

                if addr.address_line1 is None and addr.state_or_region is None:
                    response_builder.speak(NO_ADDRESS)
                else:
                    response_builder.speak(ADDRESS_AVAILABLE.format(
                        addr.address_line1, addr.state_or_region, addr.postal_code))
                return response_builder.response
            except ServiceException:
                response_builder.speak(ERROR)
                return response_builder.response
            except Exception as e:
                raise e

DirectiveServiceClient
----------------------

``DirectiveServiceClient`` can be used to send directives to `Progressive Response API <https://developer.amazon.com/docs/custom-skills/send-the-user-a-progressive-response.html>`_.
Progressive responses can be used to keep the user engaged while your skill
prepares a full response to the user's request.

Interface
~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.directive.DirectiveServiceClient:
        def enqueue(self, send_directive_request):
            # type: (SendDirectiveRequest) -> Union[Error]

    class ask_sdk_model.services.directive.SendDirectiveRequest:
        def __init__(self, header=None, directive=None):
            # type: (Optional[Header], Optional[SpeakDirective]) -> None

    class ask_sdk_model.services.directive.SpeakDirective:
        def __init__(self, speech=None):
            # type: (Optional[str]) -> None

More information on the models can be found `here <models/ask_sdk_model.services.directive.html>`__.

Code Sample
~~~~~~~~~~~

The following example shows a function that can be used in a ``handle`` method
for sending a progressive response.

.. code-block:: python

    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_model.services.directive import (
        SendDirectiveRequest, Header, SpeakDirective)
    import time

    def get_progressive_response(handler_input):
        # type: (HandlerInput) -> None
        request_id_holder = handler_input.request_envelope.request.request_id
        directive_header = Header(request_id=request_id_holder)
        speech = SpeakDirective(speech="Ok, give me a minute")
        directive_request = SendDirectiveRequest(
            header=directive_header, directive=speech)

        directive_service_client = handler_input.service_client_factory.get_directive_service()
        directive_service_client.enqueue(directive_request)
        time.sleep(5)
        return

ListManagementServiceClient
---------------------------

``ListManagementServiceClient`` can be used to access the `List Management API <https://developer.amazon.com/docs/custom-skills/access-the-alexa-shopping-and-to-do-lists.html#list-management-quick-reference>`_
n order to read or modify both the Alexa default lists and any custom lists
customer may have.

Interface
~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.list_management.ListManagementServiceClient:
        def get_lists_metadata(self):
            # type: () -> Union[ForbiddenError, Error, AlexaListsMetadata]

        def get_list(self, list_id, status):
            # type: (str, str) -> Union[AlexaList, Error]

        def get_list_item(self, list_id, item_id):
            # type: (str, str) -> Union[AlexaListItem, Error]

        def create_list(self, create_list_request):
            # type: (CreateListRequest) -> Union[Error, AlexaListMetadata]

        def create_list_item(self, list_id, create_list_item_request):
            # type: (str, CreateListItemRequest) -> Union[AlexaListItem, Error]

        def update_list(self, list_id, update_list_request):
            # type: (str, UpdateListRequest) -> Union[Error, AlexaListMetadata]

        def update_list_item(self, list_id, item_id, update_list_item_request):
            # type: (str, str, UpdateListItemRequest) -> Union[AlexaListItem, Error]

        def delete_list(self, list_id):
            # type: (str) -> Union[Error]

        def delete_list_item(self, list_id, item_id):
            # type: (str, str) -> Union[Error]


More information on the models can be found `here <models/ask_sdk_model.services.list_management.html>`__.

MonetizationServiceClient
-------------------------

In-Skill Purchase Service
~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK provides a ``MonetizationServiceClient`` that invokes `inSkillPurchase API <https://developer.amazon.com/docs/in-skill-purchase/isp-overview.html>`_
to retrieve all in-skill products associated with the current skill along
with indications if each product is purchasable and/or already purchased by
the current customer.

Interface
*********

.. code-block:: python

    class ask_sdk_model.services.monetization.MonetizationServiceClient:
        def get_in_skill_products(
            self, accept_language, purchasable=None, entitled=None,
            product_type=None, next_token=None, max_results=None):
            # type: (str, Optional[PurchasableState], Optional[EntitledState], Optional[ProductType], Optional[str], Optional[float]) -> Union[Error, InSkillProductsResponse]

        def get_in_skill_product(self, accept_language, product_id):
            # type: (str, str) -> Union[Error, InSkillProduct]

    class ask_sdk_model.services.monetization.InSkillProductsResponse:
        def __init__(self, in_skill_products=None, is_truncated=None, next_token=None):
            # type: (Optional[List[InSkillProduct]], Optional[bool], Optional[str]) -> None

    class ask_sdk_model.services.monetization.InSkillProduct:
    self, product_id=None, reference_name=None, name=None, object_type=None, summary=None, purchasable=None, entitled=None, active_entitlement_count=None, purchase_mode=None
        def __init__(
            self, product_id=None, reference_name=None, name=None,
            object_type=None, summary=None, purchasable=None, entitled=None,
            active_entitlement_count=None, purchase_mode=None):
            # type: (Optional[str], Optional[str], Optional[str], Optional[ProductType], Optional[str], Optional[PurchasableState], Optional[EntitledState], Optional[int], Optional[PurchaseMode]) -> None

    class ask_sdk_model.services.monetization.ProductType(Enum):
        SUBSCRIPTION = "SUBSCRIPTION"
        ENTITLEMENT = "ENTITLEMENT"
        CONSUMABLE = "CONSUMABLE"

    class ask_sdk_model.services.monetization.PurchasableState(Enum):
        PURCHASABLE = "PURCHASABLE"
        NOT_PURCHASABLE = "NOT_PURCHASABLE"

    class ask_sdk_model.services.monetization.EntitledState(Enum):
        ENTITLED = "ENTITLED"
        NOT_ENTITLED = "NOT_ENTITLED"

    class ask_sdk_model.services.monetization.PurchaseMode(Enum):
        TEST = "TEST"
        LIVE = "LIVE"


.. note::

    ``accept_language`` is the locale of the request and can be retrieved from
    ``handler_input.request_envelope.request.locale``.

More information on the models can be found `here <models/ask_sdk_model.services.monetization.html>`__.

Code Sample
***********

get_in_skill_products
_____________________

The ``get_in_skill_products`` method retrieves all associated in-skill
products for the current skill along with purchasability and entitlement
indications for each in-skill product for the current skill and customer.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.utils import is_request_type
    from ask_sdk_model.response import Response
    from ask_sdk_model.services.monetization import (
        EntitledState, PurchasableState, InSkillProductsResponse)

    class LaunchRequestHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return is_request_type("LaunchRequest")(handler_input)

        def handle(self, handler_input):
            locale = handler_input.request_envelope.request.locale
            ms = handler_input.service_client_factory.get_monetization_service()
            product_response = ms.get_in_skill_products(locale)

            if isinstance(product_response, InSkillProductsResponse):
                total_products = len(product_response.in_skill_products)
                entitled_products = len([l for l in product_response.in_skill_products
                                     if l.entitled == EntitledState.ENTITLED])
                purchasable_products = len([l for l in product_response.in_skill_products
                                        if l.purchasable == PurchasableState.PURCHASABLE])

                speech = (
                    "Found total {} products of which {} are purchasable and {} "
                    "are entitled".format(
                        total_products, purchasable_products, entitled_products))
            else:
                speech = "Something went wrong in loading your purchase history."

            return handler_input.response_builder.speak(speech).response

The API response contains an array of in-skill product records.

get_in_skill_product:
_____________________

The ``get_in_skill_product`` API retrieves the product record for a
single in-skill product identified by a given productId.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.utils import is_request_type
    from ask_sdk_model.response import Response
    from ask_sdk_model.services.monetization import InSkillProduct

    class LaunchRequestHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return is_request_type("LaunchRequest")(handler_input)

        def handle(self, handler_input):
            locale = handler_input.request_envelope.request.locale
            ms = handler_input.service_client_factory.get_monetization_service()
            product_id = "amzn1.adg.product.<GUID>"
            product_response = ms.get_in_skill_product(locale)

            if isinstance(product_response, InSkillProduct):
                # code to handle InSkillProduct goes here
                speech = ""
                pass
            else:
                speech = "Something went wrong in loading your product."

            return handler_input.response_builder.speak(speech).response


The API response contains a single in-skill product record.

More information on these APIs and their usage for skill implementation is
available here: `Add In-Skill Purchases to a Custom Skill <https://developer.amazon.com/docs/in-skill-purchase/add-isps-to-a-skill.html>`__.

In-Skill Purchase Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK provides the ``set_directive()`` `method <RESPONSE_BUILDING.html#interface>`__
for skills to initiate in-skill purchase and cancellation requests through
Alexa. Amazon systems then manage the voice interaction with customers, handle
the purchase transaction and return a status response back to the requesting
skill. Three different ``actions`` are supported using this interface:

 - ``Upsell``
 - ``Buy``
 - ``Cancel``

More details about these ``actions`` and recommended use-cases is available
here: `Add In-Skill Purchases to a Custom Skill <https://developer.amazon.com/docs/in-skill-purchase/add-isps-to-a-skill.html>`__.

Code Sample
***********

Upsell
______

Skills should initiate the Upsell action to present an in-skill contextually
when the user did not explicitly ask for it. E.g. During or after the free
content has been served. A productId and upsell message is required to
initiate the Upsell action. The upsell message allows developers to specify
how Alexa can present the in-skill product to the user before presenting the
pricing offer.

.. code-block:: python

    from ask_sdk_model.interfaces.connections import SendRequestDirective

    # In the skill flow, once a decision is made to offer an in-skill product to a
    # customer without an explicit ask from the customer


    return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name="Upsell",
                payload={
                    "InSkillProduct": {
                        "productId": "<product_id>",
                    },
                    "upsellMessage": "<introductory upsell description for the in-skill product>",
                },
                token="correlationToken")
        ).response

Buy
___

Skills should initiate the Buy action when a customer asks to buy a specific
in-skill product. A product_id is required to initiate the Buy action.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.utils import is_intent_name
    from ask_sdk_model.response import Response
    from ask_sdk_model.interfaces.connections import SendRequestDirective

    # Skills would implement a custom intent (BuyProductIntent below) that captures
    # user's intent to buy an in-skill product and then trigger the Buy request for it.
    # For e.g. 'Alexa, buy <product name>'

    class BuyProductIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("BuyProductIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response

            # Obtain the corresponding product_id for the requested in-skill
            # product by invoking InSkillProducts API.
            # The slot variable product_name used below is only for demonstration.

            locale = handler_input.request_envelope.request.locale
            ms = handler_input.service_client_factory.get_monetization_service()

            product_response = ms.get_in_skill_products(locale)
            slots = handler_input.request_envelope.request.intent.slots
            product_ref_name = slots.get("product_name").value
            product_record = [l for l in product_response.in_skill_products
                              if l.reference_name == product_ref_name]

            if product_record:
                return handler_input.response_builder.add_directive(
                    SendRequestDirective(
                        name="Buy",
                        payload={
                            "InSkillProduct": {
                                "productId": product_record[0].product_id
                            }
                        },
                        token="correlationToken")
                ).response
            else:
                return handler_input.response_builder.speak(
                    "I am sorry. That product is not available for purchase"
                    ).response

Cancel
______


Skills should initiate the Cancel action when a customer asks to cancel an
existing Entitlement or Subscription for a supported in-skill product. A
product_id is required to initiate the Cancel action.

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.utils import is_intent_name
    from ask_sdk_model.response import Response
    from ask_sdk_model.interfaces.connections import SendRequestDirective

    # Skills would implement a custom intent (CancelProductIntent below) that captures
    # user's intent to cancel an in-skill product and then trigger the Cancel request for it.
    # For e.g. 'Alexa, cancel <product name>'

    class CancelProductIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("CancelProductIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response

            # Obtain the corresponding product_id for the requested in-skill
            # product by invoking InSkillProducts API.
            # The slot variable product_name used below is only for demonstration.

            locale = handler_input.request_envelope.request.locale
            ms = handler_input.service_client_factory.get_monetization_service()

            product_response = ms.get_in_skill_products(locale)
            slots = handler_input.request_envelope.request.intent.slots
            product_ref_name = slots.get("product_name").value
            product_record = [l for l in product_response.in_skill_products
                              if l.reference_name == product_ref_name]

            if product_record:
                return handler_input.response_builder.add_directive(
                    SendRequestDirective(
                        name="Cancel",
                        payload={
                            "InSkillProduct": {
                                "productId": product_record[0].product_id
                            }
                        },
                        token="correlationToken")
                ).response
            else:
                return handler_input.response_builder.speak(
                    "I am sorry. I don't know that one").response

UpsServiceClient
----------------

``UpsServiceClient`` can be used to query `Alexa Customer Profile API <https://developer.amazon.com/docs/custom-skills/request-customer-contact-information-for-use-in-your-skill.html>`_
for customer contact information and `Alexa Customer Settings API <https://developer.amazon.com/docs/smapi/alexa-settings-api-reference.html>`__
for retrieving customer preferences for the time zone, distance measuring
unit and temperature measurement unit.

Interface
~~~~~~~~~

.. code-block:: python

    class ask_sdk_model.services.ups.UpsServiceClient:
        def get_profile_email(self):
            # type: () -> Union[str, Error]

        def get_profile_given_name(self):
            # type: () -> Union[str, Error]

        def get_profile_mobile_number(self):
            # type: () -> Union[PhoneNumber, Error]

        def get_profile_name(self):
            # type: () -> Union[str, Error]

        def get_system_distance_units(self, device_id):
            # type: (str) -> Union[Error, DistanceUnits]

        def get_system_temperature_unit(self, device_id):
            # type: (str) -> Union[TemperatureUnit, Error]

        def get_system_time_zone(self, device_id):
            # type: (str) -> Union[str, Error]

    class ask_sdk_model.services.ups.PhoneNumber:
        def __init__(self, country_code=None, phone_number=None):
            # type: (Optional[str], Optional[str]) -> None

    class ask_sdk_model.services.DistanceUnits(Enum):
        METRIC = "METRIC"
        IMPERIAL = "IMPERIAL"

    class ask_sdk_model.services.TemparatureUnit(Enum):
        CELSIUS = "CELSIUS"
        FAHRENHEIT = "FAHRENHEIT"

.. note::

    The device_id can be retrieved from ``handler_input.request_envelope.context.system.device.device_id``.

More information on the models can be found `here <models/ask_sdk_model.services.ups.html>`__.

