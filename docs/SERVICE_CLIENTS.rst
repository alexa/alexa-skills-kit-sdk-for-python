Alexa Service Clients
=====================

The SDK includes service clients that you can use to call Alexa APIs
from within your skill logic.

Service clients can be used in any request handler, exception handler,
and request, response interceptors. The ``service_client_factory``
contained inside the `Handler Input <REQUEST_PROCESSING.html#handler-input>`_
allows you to retrieve client instances for every supported Alexa service. The
``service_client_factory`` is only available for use, when you
`configure the skill instance <SKILL_BUILDERS.html#skill-builders>`_
with an ``ApiClient``.

The following example shows the ``handle`` function for a request
handler that creates an instance of the device address service client.
Creating a service client instance is as simple as calling the
appropriate factory function.

.. code:: python

    def handle(handler_input):
        device_id = handler_input.request_envelope.context.system.device.device_id
        device_addr_service_client = handler_input.service_client_factory.get_device_address_service()
        addr = device_addr_service_client.get_full_address(device_id)
        # Other handler logic goes here
        ....

