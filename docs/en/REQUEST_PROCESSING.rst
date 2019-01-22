Request Processing
******************

Standard Request
================

Alexa communicates with the skill service via a request-response mechanism
using HTTP over SSL/TLS. When a user interacts with an Alexa skill, your
service receives a POST request containing a JSON body. The request body
contains the parameters necessary for the service to perform its logic and
generate a JSON-formatted response. The documentation on JSON structure of
the request body can be found `here <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#request-format>`_.

Though Python can handle JSON natively as ``dict`` objects, for providing type
support, they are deserialized into model objects (``ask-sdk-model`` package)
for skill consumption.


Handler Input
=============

Request Handlers, Request and Response Interceptors, and Exception Handlers
are all passed a global ``HandlerInput`` object during invocation. This object
exposes various entities useful in request processing, including:

    -  **request_envelope**: Contains the entire `request
       body <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#request-body-syntax>`_
       sent to skill.
    -  **attributes_manager**: Provides access to request, session, and
       persistent attributes.
    -  **service_client_factory**: Constructs service clients capable of
       calling Alexa APIs.
    -  **response_builder**: Contains helper function to build responses.
    -  **context**: Provides an optional, context object passed in by the
       host container. For example, for skills running on AWS Lambda, this
       is the `context
       object <https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html>`_
       for the AWS Lambda function.

Request Handlers
================

Request handlers are responsible for handling one or more types of
incoming alexa requests. There are two ways of creating custom request
handlers:

- By implementing the ``AbstractRequestHandler`` class.
- By decorating a custom handle function using the
  `Skill Builder <SKILL_BUILDERS.html#skill-builder>`__ ``request_handler``
  decorator.

.. warning::

    You may use either implementation using **classes**
    or **decorators** to write a skill.

    We strongly recommend you to choose
    **one** of the options and use it consistently throughout your skill, for
    better code structure.

Interface
---------

.. tabs::

    .. tab:: AbstractRequestHandler Class

        If you plan on using the ``AbstractRequestHandler`` class, you will
        need to implement the following methods :

        -  **can_handle**:  ``can_handle`` method is called by the SDK to
           determine if the given handler is capable of processing the incoming
           request. This function accepts a `Handler Input <#handler-input>`__
           object and expects a boolean to be returned. If the method returns
           **True**, then the handler is supposed to handle the request
           successfully. If it returns **False**, the handler is not supposed
           to handle the input request and hence not executed to completion.
           Because of the various attributes in ``HandlerInput`` object, you
           can write any condition to let SDK know whether the request can be
           handled gracefully or not.
        -  **handle**: ``handle`` method is called by the SDK when invoking the
           request handler. This function contains the handler’s request
           processing logic, accepts `Handler Input <#handler-input>`__ and
           returns a ``Response`` object.

        .. code:: python

            class AbstractRequestHandler(object):
                @abstractmethod
                def can_handle(self, handler_input):
                    # type: (HandlerInput) -> bool
                    pass

                @abstractmethod
                def handle(self, handler_input):
                    # type: (HandlerInput) -> Response
                    pass

    .. tab:: RequestHandler Decorator

        The ``request_handler`` decorator from SkillBuilder class is a custom wrapper
        on top of the ``AbstractRequestHandler`` class and provides the same
        functionality to any custom decorated function. However, there are couple of
        things to take into consideration, before using the decorator:

        - The decorator expects a ``can_handle_func`` parameter. This is similar to
          the ``can_handle`` method in ``AbstractRequestHandler``. The value passed
          should be a function that accepts a `Handler Input <#handler-input>`__
          object and returns a ``boolean`` value
        - The decorated function should accept only one parameter, which is the
          `Handler Input <#handler-input>`__ object and may return a ``Response``
          object.

        .. code:: python

            class SkillBuilder(object):
                ....
                def request_handler(self, can_handle_func):
                    def wrapper(handle_func):
                        # wrap the can_handle and handle into a class
                        # add the class into request handlers list
                        ....
                    return wrapper

Code Sample
-----------

The following example shows a request handler class that can handle the
``HelloWorldIntent``.

    .. tabs::

        .. tab:: AbstractRequestHandler Class

            .. code:: python

              from ask_sdk_core.dispatch_components import AbstractRequestHandler
              from ask_sdk_core.utils import is_intent_name
              from ask_sdk_model.ui import SimpleCard

              class HelloWorldIntentHandler(AbstractRequestHandler):
                  def can_handle(self, handler_input):
                      return is_intent_name("HelloWorldIntent")(handler_input)

                  def handle(self, handler_input):
                      speech_text = "Hello World";

                      return handler_input.response_builder.speak(speech_text).set_card(
                          SimpleCard("Hello World", speech_text)).response

            The ``can_handle`` function detects if the incoming request is an
            ``IntentRequest`` and returns true if the intent name is
            ``HelloWorldIntent``. The ``handle`` function generates and returns a
            basic "Hello World" response.

        .. tab:: RequestHandler Decorator

            .. code-block:: python

                from ask_sdk_core.utils import is_intent_name
                from ask_sdk_model.ui import SimpleCard
                from ask_sdk_core.skill_builder import SkillBuilder

                sb = SkillBuilder()

                @sb.request_handler(can_handle_func = is_intent_name("HelloWorldIntent"))
                def hello_world_intent_handler(handler_input):
                    speech_text = "Hello World!"

                    return handler_input.response_builder.speak(speech_text).set_card(
                        SimpleCard("Hello World", speech_text)).response

            The ``is_intent_name`` function accepts a ``string`` parameter and returns an
            anonymous function which accepts a ``HandlerInput`` as input parameter and
            checks if the incoming request in ``HandlerInput`` is an ``IntentRequest`` and
            returns if the intent name is the passed in ``string``, which is
            ``HelloWorldIntent`` in this example. The ``handle`` function generates and returns a
            basic "Hello World" response.

Registering and Processing the Request Handlers
-----------------------------------------------

The SDK calls the ``can_handle`` function on its request handlers in the
order in which they were provided to the ``Skill`` builder.

.. tabs::

    .. tab:: AbstractRequestHandler Class

        If you are following the ``AbstractRequestHandler`` class approach, then
        you can register the request handlers in the following way

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # Implement FooHandler, BarHandler, BazHandler classes

            sb.request_handlers.extend([
                    FooHandler(),
                    BarHandler(),
                    BazHandler()])

    .. tab:: RequestHandler Decorator

        If you are following the ``request_handler`` decorator approach, then
        there is no need to explicitly register the handler functions, since
        they are already decorated using a skill builder instance.

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # decorate foo_handler, bar_handler, baz_handler functions

.. note::

    In the above example, the SDK calls request handlers in the following order:

    1. ``FooHandler`` class / ``foo_handler`` function
    2. ``BarHandler`` class / ``bar_handler`` function
    3. ``BazHandler`` class / ``baz_handler`` function

    The SDK always chooses the first handler that is capable of handling a
    given request. In this example, if both ``FooHandler`` class /``foo_handler`` function
    and ``BarHandler`` class /``bar_handler`` function are capable of handling a particular
    request, ``FooHandler`` class /``foo_handler`` function is always invoked.
    Keep this in mind when designing and registering request handlers.


Exception Handlers
==================

Exception handlers are similar to request handlers, but are instead
responsible for handling one or more types of exceptions. They are invoked
by the SDK when an unhandled exception is thrown during the course of
request processing.

In addition to the `Handler Input <#handler-input>`__ object, the handler
also has access to the exception raised during handling the input
request, thus making it easier for the handler to figure out how to
handle the corresponding exception.

Similar to `Request Handlers <#request-handlers>`_, custom
request interceptors can be implemented in two ways:

- By implementing the ``AbstractExceptionHandler`` class.
- By decorating a custom exception handling function using the
  `Skill Builder <SKILL_BUILDERS.html##skill-builders>`__
  ``exception_handler`` decorator.

.. warning::

    You may use either implementation using **classes**
    or **decorators** to write a skill.

    We strongly recommend you to choose
    **one** of the options and use it consistently throughout your skill, for
    better code structure.

Interface
---------

.. tabs::

    .. tab:: AbstractExceptionHandler Class

        If you plan on using the ``AbstractExceptionHandler`` class, you will
        need to implement the following methods :

        -  **can_handle**: ``can_handle`` method, which is called by the SDK
           to determine if the given handler is capable of handling the exception.
           This function returns **True** if the handler can handle the exception,
           or **False** if not. Return ``True`` in all cases to create a catch-all
           handler.
        -  **handle**: ``handle`` method, which is called by the SDK when invoking
           the exception handler. This function contains all exception handling logic,
           and returns a ``Response`` object.

        .. code:: python

            class AbstractExceptionHandler(object):
                @abstractmethod
                def can_handle(self, handler_input, exception):
                    # type: (HandlerInput, Exception) -> bool
                    pass

                @abstractmethod
                def handle(self, handler_input, exception):
                    # type: (HandlerInput, Exception) -> Response
                    pass

    .. tab:: ExceptionHandler Decorator

        The ``exception_handler`` decorator from SkillBuilder class is a custom wrapper
        on top of the ``AbstractExceptionHandler`` class and provides the same
        functionality to any custom decorated function. However, there are couple of
        things to take into consideration, before using the decorator:

        - The decorator expects a ``can_handle_func`` parameter. This is similar to
          the ``can_handle`` method in ``AbstractExceptionHandler``. The value passed
          should be a function that accepts a `Handler Input <#handler-input>`__
          object, an ``Exception`` instance and returns a ``boolean`` value.
        - The decorated function should accept only two parameters, the
          `Handler Input <#handler-input>`__ object and ``Exception`` object. It may
          return a ``Response`` object.

        .. code:: python

            class SkillBuilder(object):
                ....
                def exception_handler(self, can_handle_func):
                    def wrapper(handle_func):
                        # wrap the can_handle and handle into a class
                        # add the class into exception handlers list
                        ....
                    return wrapper

Code Sample
-----------
The following example shows an exception handler that can handle any exception
with name that contains “AskSdk”.

.. tabs::

    .. tab:: AbstractExceptionHandler Class

        .. code:: python

            class AskExceptionHandler(AbstractExceptionHandler):
                def can_handle(self, handler_input, exception):
                    return 'AskSdk' in exception.__class__.__name__

                def handle(self, handler_input, exception):
                    speech_text = "Sorry, I am unable to figure out what to do. Try again later!!"

                    return handler_input.response_builder.speak(speech_text).response

        The handler’s ``can_handle`` method returns True if the incoming exception
        has a name that starts with “AskSdk”. The ``handle`` method returns a
        graceful exception response to the user.

    .. tab:: ExceptionHandler Decorator

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            @sb.exception_handler(can_handle_func = lambda i, e: 'AskSdk' in e.__class__.__name__)
            def ask_exception_intent_handler(handler_input, exception):
                speech_text = "Sorry, I am unable to figure out what to do. Try again later!!"

                return handler_input.response_builder.speak(speech_text).response


Registering and Processing the Exception Handlers
-------------------------------------------------

.. tabs::

    .. tab:: AbstractExceptionHandler Class

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # Implement FooExceptionHandler, BarExceptionHandler, BazExceptionHandler classes

            sb.add_exception_handler(FooExceptionHandler())
            sb.add_exception_handler(BarExceptionHandler())
            sb.add_exception_handler(BazExceptionHandler())

    .. tab:: ExceptionHandler Decorator

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # decorate foo_exception_handler, bar_exception_handler, baz_exception_handler functions

.. note::

    Like request handlers, exception handlers are executed in the order in which
    they were registered to the Skill.

Request and Response Interceptors
=================================

The SDK supports Global Request and Response Interceptors that execute
**before** and **after** matching ``RequestHandler`` execution, respectively.

Request Interceptors
--------------------

The Global Request Interceptor accepts a `Handler Input <handler-input>`__
object and processes it, before processing any of the registered request
handlers. Similar to `Request Handlers <#request-handlers>`_, custom
request interceptors can be implemented in two ways:

- By implementing the ``AbstractRequestInterceptor`` class.
- By decorating a custom process function using the
  `Skill Builder <SKILL_BUILDERS.html##skill-builder>`__
  ``global_request_interceptor`` decorator.

.. warning::

    You may use either implementation using **classes**
    or **decorators** to write a skill.

    We strongly recommend you to choose
    **one** of the options and use it consistently throughout your skill, for
    better code structure.

Interface
~~~~~~~~~

.. tabs::

    .. tab:: AbstractRequestInterceptor Class

        The ``AbstractRequestInterceptor`` class usage needs you to implement the
        ``process`` method. This method takes a `Handler Input <#handler-input>`__
        instance and doesn't return anything.

        .. code:: python

            class AbstractRequestInterceptor(object):
                @abstractmethod
                def process(self, handler_input):
                    # type: (HandlerInput) -> None
                    pass

    .. tab:: GlobalRequestInterceptor Decorator

        The ``global_request_interceptor`` decorator from SkillBuilder class is a custom
        wrapper on top of the ``AbstractRequestInterceptor`` class and provides the same
        functionality to any custom decorated function. However, there are couple of
        things to take into consideration, before using the decorator:

        - The decorator should be invoked as a function rather than as a function name,
          since it requires the skill builder instance, to register the interceptor.
        - The decorated function should accept only one parameter, which is the
          `Handler Input <#handler-input>`__ object and the return value from the function
          is not captured.

        .. code:: python

            class SkillBuilder(object):
                ....
                def global_request_interceptor(self):
                    def wrapper(process_func):
                        # wrap the process_func into a class
                        # add the class into request interceptors list
                        ....
                    return wrapper

Code Sample
~~~~~~~~~~~

The following example shows a request interceptor class that can print the
request received by Alexa service, in AWS CloudWatch logs, before handling it.

.. tabs::

    .. tab:: AbstractRequestInterceptor Class

        .. code:: python

            from ask_sdk_core.dispatch_components import AbstractRequestInterceptor

            class LoggingRequestInterceptor(AbstractRequestInterceptor):
                def process(self, handler_input):
                    print("Request received: {}".format(handler_input.request_envelope.request))

    .. tab:: GlobalRequestInterceptor Decorator

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            @sb.global_request_interceptor()
            def request_logger(handler_input):
                print("Request received: {}".format(handler_input.request_envelope.request))


Registering and Processing the Request Interceptors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Request interceptors are invoked immediately before execution of the request handler
for an incoming request. Request attributes in `Handler Input <#handler-input>`__'s
``Attribute Manager`` provide a way for request interceptors to pass data and entities
on to other request interceptors and request handlers.

.. tabs::

    .. tab:: AbstractRequestInterceptor Class

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # Implement FooInterceptor, BarInterceptor, BazInterceptor classes

            sb.add_global_request_interceptor(FooInterceptor())
            sb.add_global_request_interceptor(BarInterceptor())
            sb.add_global_request_interceptor(BazInterceptor())

    .. tab:: GlobalRequestInterceptor Decorator

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()
            # decorate foo_interceptor, bar_interceptor, baz_interceptor functions

.. note::

    In the above example, the SDK executes all request interceptors in the following order:

    1. ``FooInterceptor`` class / ``foo_interceptor`` function
    2. ``BarInterceptor`` class / ``bar_interceptor`` function
    3. ``BazInterceptor`` class / ``baz_interceptor`` function


Response Interceptors
---------------------

The Global Response Interceptor accepts a `Handler Input <#handler-input>`__
object, a `Response` and processes them, after executing the supported request
handler. Similar to `Request Interceptors <#request-interceptors>`_, custom
response interceptors can be implemented in two ways:

- By implementing the ``AbstractResponseInterceptor`` class.
- By decorating a custom process function using the
  `Skill Builder <SKILL_BUILDERS.html#skill-builders>`__
  ``global_response_interceptor`` decorator.

.. warning::

    You may use either implementation using **classes**
    or **decorators** to write a skill.

    We strongly recommend you to choose
    **one** of the options and use it consistently throughout your skill, for
    better code structure.

Interface
~~~~~~~~~

.. tabs::

    .. tab:: AbstractResponseInterceptor Class

        The ``AbstractResponseInterceptor`` class usage needs you to implement the
        ``process`` method. This method takes a `Handler Input <#handler-input>`__
        instance, a ``Response`` object that is returned from the previously executed
        request handler. The method doesn't return anything.

        .. code:: python

            class AbstractResponseInterceptor(object):
                @abstractmethod
                def process(self, handler_input, response):
                    # type: (HandlerInput, Response) -> None
                    pass

    .. tab:: GlobalResponseInterceptor Decorator

        The ``global_response_interceptor`` decorator from SkillBuilder class is a custom
        wrapper on top of the ``AbstractResponseInterceptor`` class and provides the same
        functionality to any custom decorated function. However, there are couple of
        things to take into consideration, before using the decorator:

        - The decorator should be invoked as a function rather than as a function name,
          since it requires the skill builder instance, to register the interceptor.
        - The decorated function should accept two parameters, which are the
          `Handler Input <#handler-input>`__ object and ``Response`` object respectively.
          The return value from the function is not captured.

        .. code:: python

            class SkillBuilder(object):
                ....
                def global_response_interceptor(self):
                    def wrapper(process_func):
                        # wrap the process_func into a class
                        # add the class into response interceptors list
                        ....
                    return wrapper

Code Sample
~~~~~~~~~~~

The following example shows a response interceptor class that can print the
response received from successfully handling the request, in AWS CloudWatch logs,
before returning it to the Alexa Service.

.. tabs::

    .. tab:: AbstractRequestInterceptor Class

        .. code:: python

          from ask_sdk_core.dispatch_components import AbstractResponseInterceptor

          class LoggingResponseInterceptor(AbstractResponseInterceptor):
              def process(handler_input, response):
                  print("Response generated: {}".format(response))

    .. tab:: GlobalRequestInterceptor Decorator

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            @sb.global_response_interceptor()
            def response_logger(handler_input, response):
                print("Response generated: {}".format(response))


Registering and Processing the Response Interceptors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Response interceptors are invoked immediately after execution of the request handler
for an incoming request.

.. tabs::

    .. tab:: AbstractRequestInterceptor Class

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # Implement FooInterceptor, BarInterceptor, BazInterceptor classes

            sb.add_global_response_interceptor(FooInterceptor())
            sb.add_global_response_interceptor(BarInterceptor())
            sb.add_global_response_interceptor(BazInterceptor())

    .. tab:: GlobalRequestInterceptor Decorator

        .. code-block:: python

            from ask_sdk_core.skill_builder import SkillBuilder

            sb = SkillBuilder()

            # decorate foo_interceptor, bar_interceptor, baz_interceptor functions

.. note::

    Similar to the processing of `Request Interceptors <#request-interceptors>`_,
    all of the response interceptors are executed in the same order they are registered.
