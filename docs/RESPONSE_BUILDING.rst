ResponseBuilder
===============

The SDK includes helper functions for constructing responses. A
``Response`` may contain multiple elements, and the helper functions aid
in generating responses, reducing the need to initialize and set the
elements of each response.

Interface
~~~~~~~~~

.. code:: python

    class ResponseFactory(object):
        def __init__(self):
            self.response = ....  # Response object

        def speak(self, speech):
            # type: (str) -> 'ResponseFactory'
            ....

        def ask(self, speech):
            # type: (str) -> 'ResponseFactory'
            ....

        def set_card(self, card):
            # type: (Card) -> 'ResponseFactory'
            ....

        def set_directive(self, directive):
            # type: (Directive) -> 'ResponseFactory'
            ....

        def set_should_end_session(self, end_session):
            # type: (bool) -> 'ResponseFactory'
            ....

The following example shows how to construct a response using
``ResponseFactory`` helper functions.

.. code:: python

    def handle(handler_input):
        handler_input.response_builder.speak('foo').ask('bar').set_card(
            SimpleCard('title', 'content'))
        return handler_input.response_builder.response

Text Helpers
~~~~~~~~~~~~

The following helper functions are provided to skill developers, to
help with text content generation:

get_plain_text_content
----------------------

.. code:: python

    def get_plain_text_content(primary_text, secondary_text, tertiary_text):
        # type: (str, str, str) -> TextContent
        # Create a text content object with text as PlainText type
        ....


get_rich_text_content
----------------------

.. code:: python

    def get_rich_text_content(primary_text, secondary_text, tertiary_text):
        # type: (str, str, str) -> TextContent
        # Create a text content object with text as RichText type
        ....


get_text_content
----------------------

.. code:: python

    def get_text_content(
        primary_text, primary_text_type,
        secondary_text, secondary_text_type,
        tertiary_text, tertiary_text_type):
        # type: (str, str, str, str, str, str) -> TextContent
        # Create a text content object with text as corresponding passed-type
        # Passed-in type is defaulted to PlainText
        ....
