レスポンスビルディング
===================

SDKには、 ``ResponseFactory`` クラスが含まれています。このクラスにはヘルパー
応答を構築するための関数。``Response`` には複数の要素が含まれる場合があり、ヘルパー関数によって応答を生成しやすくなり、各応答の要素を初期化したり設定したりする時間を削減できます。

インターフェース
~~~~~~~~~~~~~~

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

        def add_directive(self, directive):
            # type: (Directive) -> 'ResponseFactory'
            ....

        def set_should_end_session(self, end_session):
            # type: (bool) -> 'ResponseFactory'
            ....

``ResponseFactory`` クラスのインスタンスである ``response_builder`` は、
スキル開発者に
`HandlerInput <REQUEST_PROCESSING.html#id2>`_ オブジェクトを返します。
スキルコンポーネントに渡される標準引数です。

.. note::

    - 異なるディレクティブを使用して追加するには、`directive <models/ask_sdk_model.html＃ask_sdk_model.directive.Directive>`__ モデル定義。
    - カードを使用して設定するには、`Card <models/ask_sdk_model.ui.html＃ask_sdk_model.ui.card.Card>`__ モデル定義。

以下は、``ResponseFactory`` ヘルパー関数を使用して応答を作成する方法の例です。

.. code:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_core.utils import is_intent_name
    from ask_sdk_core.response_helper import get_plain_text_content

    from ask_sdk_model.response import Response
    from ask_sdk_model.interfaces.display import (
        ImageInstance, Image, RenderTemplateDirective,
        BackButtonBehavior, BodyTemplate2)
    from ask_sdk_model import ui

    class HelloIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("HelloIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            response_builder = handler_input.response_builder

            speech = "This is a sample response"

            response_builder.set_card(
                ui.StandardCard(
                    title="Card Title",
                    text="Hey this is a sample card",
                    image=ui.Image(
                        small_image_url="<Small Image URL>",
                        large_image_url="<Large Image URL>"
                    )
                )
            )

            if supports_display(handler_input):
                img = Image(
                    sources=[ImageInstance(url="<Large Image URL>")])
                title = "Template Title"
                primary_text = get_plain_text_content(
                    primary_text="some text")

                response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate2(
                            back_button=BackButtonBehavior.VISIBLE,
                            image=img, title=title,
                            text_content=primary_text)))

            return response_builder.speak(speech).response

テキストヘルパー
~~~~~~~~~~~~~~

次のヘルパー関数がスキル開発者用に用意されており、テキストコンテンツの生成に役立ちます。

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
