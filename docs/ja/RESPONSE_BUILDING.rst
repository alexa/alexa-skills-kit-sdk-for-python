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

        def set_directive(self, directive):
            # type: (Directive) -> 'ResponseFactory'
            ....

        def set_should_end_session(self, end_session):
            # type: (bool) -> 'ResponseFactory'
            ....

``ResponseFactory`` クラスのインスタンスである ``response_builder`` は、
スキル開発者に
`HandlerInput <REQUEST_PROCESSING.html#id2>`_ オブジェクトを返します。
スキルコンポーネントに渡される標準引数です。

以下は、``ResponseFactory`` ヘルパー関数を使用して応答を作成する方法の例です。

.. code:: python

    def handle(handler_input):
        handler_input.response_builder.speak('foo').ask('bar').set_card(
            SimpleCard('title', 'content'))
        return handler_input.response_builder.response

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
