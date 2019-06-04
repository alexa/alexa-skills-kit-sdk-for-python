============
初めてのスキル開発
============

`セットアップ <GETTING_STARTED.html>`__\ ガイドでは、ASK
SDK for
Pythonを特定のディレクトリまたはvirtualenvを使用して仮想環境にインストールする方法を説明しました。このガイドでは、ASK
SDK for Pythonを使ったスキル開発の手順を説明します。

前提条件
--------

ASK SDK for Pythonのインストールに加えて、以下のものが必要です。

-  `Amazon開発者 <https://developer.amazon.com/>`__\ アカウント。Alexaスキルの作成と設定に必要です。
-  `アマゾンウェブサービス（AWS） <https://aws.amazon.com/>`__\ アカウント。AWS
   Lambdaでスキルをホスティングするために必要です。

Hello Worldの作成
----------------

hello_world.pyというPythonファイルにHello
Worldを作成します。先ほど作成したskillフォルダに、お好みのテキストエディターやIDEを使用してhello_world.pyという名前のファイルを作成してください。

Hello Worldの実装
----------------

リクエストハンドラー
~~~~~~~~~~

Alexaサービスによって送信されたイベントに応答するには、カスタムスキルが必要です。たとえば、Alexaデバイス（Echo、Echo
Dot、Echo
Showなど）に「ハローワールドを開いて」と頼む場合、スキルがHello
Worldスキルに送信されたLaunchRequestに応答する必要があります。ASK SDK
for
Pythonを使用すれば、リクエストハンドラーを作成するだけで済みます。リクエストハンドラーは受け取ったリクエストを処理して応答を返すコードです。このコードは受け取ったリクエストを正しいリクエストハンドラーを使用して処理し、応答を返します。ASK
SDK for
Pythonでは、次のいずれかの方法でリクエストハンドラーを作成することができます。

1. ask_sdk_core.dispatch_componentsパッケージの下にAbstractRequestHandlerクラスを実装します。このクラスにはcan_handleおよびhandleメソッドの実装が含まれている必要があります。詳細については\ `クラスを使用した実装 <#option-1-implementation-using-classes>`__\ セクションで説明しています。
2. インスタンス化されたスキルビルダーオブジェクトのrequest_handlerデコレーターを使用して、異なる受信リクエストのハンドラーとして動作するように関数をタグ付けします。詳細については\ `デコレーターを使用した実装 <#option-2-implementation-using-decorators>`__\ セクションで説明しています。

Hello
Worldスキルの実装を通じて、まずハンドラークラスの使用方法、次に同じスキルをデコレーターを使用して作成する方法を説明します。機能は同じです。\ **どちら**\ を使用してもかまいません。

例外ハンドラー
~~~~~~~~~

うまくいかないことが起こったときに、スキルコードで問題を正常に処理する方法が必要です。ASK
SDK for
Pythonは、リクエストの処理と似た方法で例外処理をサポートします。\ `クラス <#id6>`__\ または\ `デコレーター <#id14>`__\ を選んで使用できます。以下の実装セクションで、例外処理の実装方法を説明します。

.. tip::

    スキルの記述には、\ `クラスを使用した実装 <#id6>`__\ と\ `デコレーターを使用した実装 <#id14>`__\ のどちらのオプションを使用してもかまいません。

.. warning::

    コード構造を良好に保つために、\ **いずれか**\ のオプションを選択し、スキル全体で常に使用することを強くお勧めします。

オプション1： ハンドラークラスを使用した実装
---------------------------

最初にスキルビルダーオブジェクトを作成します。スキルビルダーオブジェクトは、スキルで入力されたリクエストの処理とカスタム応答の生成を担当するコンポーネントを追加するのに便利です。

以下のコードを``hello_world.py``ファイルに入力するか貼り付けます。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

ハンドラークラスを使用するには、``AbstractRequestHandler``クラスの2つのメソッド``can_handle``および``handle``を実装するクラスとして各リクエストハンドラーを作成する必要があります。

``can_handle``メソッドは、リクエストハンドラーがリクエストに対して適切な応答を作成できるかを示すブール値を返します。``can_handle``メソッドは、スキルが前回のリクエストに設定したり、前回のやり取りで保存した、リクエストタイプやそのほかのアトリビュートにアクセスできます。Hello
Worldスキルで参照する必要があるのは、各ハンドラーが受け取ったリクエストに応答できるかどうかを判断するリクエスト情報のみです。

LaunchRequestハンドラー
~~~~~~~~~~~~~~~~~~

以下は、スキルが\ `LaunchRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#launchrequest>`__\ を受け取ったときに呼び出されるハンドラーを設定するコードのサンプルです。LaunchRequestイベントは、特定のインテントなしでスキルが呼び出された場合に発生します。

以下のコードを``hello_world.py``ファイルの、前述のコードの後に入力するか貼り付けます。

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractRequestHandler
    from ask_sdk_core.utils import is_request_type, is_intent_name
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_model import Response
    from ask_sdk_model.ui import SimpleCard

    class LaunchRequestHandler(AbstractRequestHandler):
         def can_handle(self, handler_input):
             # type: (HandlerInput) -> bool
             return is_request_type("LaunchRequest")(handler_input)

         def handle(self, handler_input):
             # type: (HandlerInput) -> Response
             speech_text = "ようこそ、アレクサスキルキットへ。こんにちは、と言ってみてください。"

             handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("ハローワールド", speech_text)).set_should_end_session(
                False)
             return handler_input.response_builder.response

受け取ったリクエストがLaunchRequestの場合、can_handle関数は\ **True**\ を返します。handle関数は、基本的なあいさつの応答を生成して返します。

HelloWorldIntentハンドラー
~~~~~~~~~~~~~~~~~~~~~

以下は、スキルがHelloWorldIntentという名前のインテントリクエストを受け取った時に呼び出されるハンドラーを設定するコードのサンプルです。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    class HelloWorldIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("HelloWorldIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            speech_text = "こんにちは"

            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("ハローワールド", speech_text)).set_should_end_session(
                True)
            return handler_input.response_builder.response

can_handle関数は受け取るリクエストが\ `IntentRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#intentrequest>`__\ かどうかを検出し、インテント名がHelloWorldIntentの場合に\ **True**\ を返します。handle関数は、基本的な「こんにちは」という応答を生成して返します。

HelpIntentハンドラー
~~~~~~~~~~~~~~~

以下は、スキルがビルトインインテント\ `AMAZON.HelpIntent <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`__\ を受け取ったときに呼び出されるハンドラーを設定するコードのサンプルです。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    class HelpIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("AMAZON.HelpIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            speech_text = "こんにちは。と言ってみてください。"

            handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
                SimpleCard("ハローワールド", speech_text))
            return handler_input.response_builder.response

先ほどのハンドラー同様、このハンドラーはIntentRequestを想定されるインテント名と照合します。基本的なヘルプ手順が返され、.ask(speech_text)によってユーザーのマイクがオンになりユーザーの応答を待ちます。

CancelAndStopIntentハンドラー
~~~~~~~~~~~~~~~~~~~~~~~~

CancelAndStopIntentHandlerもビルトインインテント\ `AMAZON.CancelIntentまたはAMAZON.StopIntent <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`__\ によって呼び出されるため、HelpIntentハンドラーに似ています。以下は、1つのハンドラーを使用して両方のインテントに応答する例です。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    class CancelAndStopIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_intent_name("AMAZON.CancelIntent")(handler_input)
                     or is_intent_name("AMAZON.StopIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            speech_text = "さようなら"

            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("ハローワールド", speech_text))
            return handler_input.response_builder.response

両方のインテントに対する応答は同じであるため、1つのハンドラーにすることで重複するコードを減らせます。

SessionEndedRequestハンドラー
~~~~~~~~~~~~~~~~~~~~~~~~

`SessionEndedRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#sessionendedrequest>`__\ を受け取った後は音声、カード、ディレクティブを使った応答を返すことはできませんが、クリーンアップロジックを追加するにはSessionEndedRequestHandlerが最適な場所です。以下のコードをhello_world.pyファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    class SessionEndedRequestHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return is_request_type("SessionEndedRequest")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            # クリーンアップロジックをここに追加します

            return handler_input.response_builder.response

例外ハンドラーの実装
~~~~~~~~~~~~~~

以下は、catch
all例外ハンドラーをスキルに追加して、すべての例外に対してスキルが意味のあるメッセージを返すようにする例です。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    from ask_sdk_core.dispatch_components import AbstractExceptionHandler

    class AllExceptionHandler(AbstractExceptionHandler):

        def can_handle(self, handler_input, exception):
            # type: (HandlerInput, Exception) -> bool
            return True

        def handle(self, handler_input, exception):
            # type: (HandlerInput, Exception) -> Response
            # CloudWatch Logsに例外を記録する
            print(exception)

            speech = "すみません、わかりませんでした。もう一度言ってください。"
            handler_input.response_builder.speak(speech).ask(speech)
            return handler_input.response_builder.response

Lambdaハンドラーの作成
~~~~~~~~~~~~~~~~

.. note::

    カスタムスキルの場合、サービスは、AWS
    Lambdaでホスティングするか、独自のエンドポイントでウェブサービスとしてホスティングできます。

    一般的に、AWS
    Lambdaでスキルコードをホスティングするのが最も簡単です。以下のセクションでは、その方法を説明します。

    ただし、他のクラウドホスティングプロバイダーでホスティングする場合は、SDKにいくつか用意されているサポートパッケージ（``ask-sdk-webservice-support``、``flask-ask-sdk``、``django-ask-sdk``）を使用してください。このコンフィギュレーションについて詳しくは、\ `こちら <WEBSERVICE_SUPPORT.html>`__\ を参照してください。

`Lambda <https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html>`__\ ハンドラーは、AWS
Lambda関数のエントリポイントとなります。以下は、スキルが受信するすべてのリクエストのルーティングを行うLambdaハンドラー関数のコードサンプルです。Lambdaハンドラー関数は、作成したリクエストハンドラーを使用して設定されたSDKのスキルインスタンスを作成します。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    sb.add_request_handler(LaunchRequestHandler())
    sb.add_request_handler(HelloWorldIntentHandler())
    sb.add_request_handler(HelpIntentHandler())
    sb.add_request_handler(CancelAndStopIntentHandler())
    sb.add_request_handler(SessionEndedRequestHandler())

    sb.add_exception_handler(AllExceptionHandler())

    handler = sb.lambda_handler()

オプション2： デコレーターを使用した実装
-------------------------

以下は、上記と同じ機能を実装するコードですが、関数デコレーターを使用しています。デコレーターは、上記の各ハンドラークラスに実装された``can_handle``メソッドに代わるものと考えてください。

最初にスキルビルダーオブジェクトを作成します。スキルビルダーオブジェクトは、スキルで入力されたリクエストの処理とカスタム応答の生成を担当するコンポーネントを追加するのに便利です。

以下のコードを``hello_world.py``ファイルに入力するか貼り付けます。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

LaunchRequestハンドラー
~~~~~~~~~~~~~~~~~~

以下は、スキルが\ `LaunchRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#launchrequest>`__\ を受け取ったときに呼び出されるハンドラーを設定するコードのサンプルです。LaunchRequestイベントは、特定のインテントなしでスキルが呼び出された場合に発生します。

以下のコードを``hello_world.py``ファイルの、前述のコードの後に入力するか貼り付けます。

.. code-block:: python

    from ask_sdk_core.utils import is_request_type, is_intent_name
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_model import Response
    from ask_sdk_model.ui import SimpleCard

    @sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
    def launch_request_handler(handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "ようこそ、アレクサスキルキットへ。こんにちは、と言ってみてください。"

        handler_input.response_builder.speak(speech_text).set_card(
             SimpleCard("ハローワールド", speech_text)).set_should_end_session(
             False)
        return handler_input.response_builder.response

クラスパターンのLaunchRequestHandlerの``can_handle``関数と同様に、デコレーターは受け取るリクエストがLaunchRequestの場合に\ **True**\ を返します。``handle``関数は、クラスパターンの``handle``関数と同じ方法で基本的なあいさつの応答を生成して返します。

HelloWorldIntentハンドラー
~~~~~~~~~~~~~~~~~~~~~

以下は、スキルがHelloWorldIntentという名前のインテントリクエストを受け取った時に呼び出されるハンドラーを設定するコードのサンプルです。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    @sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
    def hello_world_intent_handler(handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "こんにちは"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("ハローワールド", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

HelpIntentハンドラー
~~~~~~~~~~~~~~~

以下は、スキルがビルトインインテント\ `AMAZON.HelpIntent <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`__\ を受け取ったときに呼び出されるハンドラーを設定するコードのサンプルです。以下のコードをhello_world.pyファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    @sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
    def help_intent_handler(handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "こんにちは。と言ってみてください。"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("ハローワールド", speech_text))
        return handler_input.response_builder.response

先ほどのハンドラー同様、このハンドラーはIntentRequestを想定されるインテント名と照合します。基本的なヘルプ手順が返され、``.ask(speech_text)``によってユーザーのマイクがオンになりユーザーの応答を待ちます。

CancelAndStopIntentハンドラー
~~~~~~~~~~~~~~~~~~~~~~~~

CancelAndStopIntentHandlerもビルトインインテント\ `AMAZON.CancelIntentまたはAMAZON.StopIntent <https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#available-standard-built-in-intents>`__\ によって呼び出されるため、HelpIntentハンドラーに似ています。以下は、1つのハンドラーを使用して両方のインテントに応答する例です。以下のコードをhello_world.pyファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    @sb.request_handler(
        can_handle_func=lambda handler_input :
            is_intent_name("AMAZON.CancelIntent")(handler_input) or
            is_intent_name("AMAZON.StopIntent")(handler_input))
    def cancel_and_stop_intent_handler(handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "さようなら"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("ハローワールド", speech_text))
        return handler_input.response_builder.response

上記の例では、``can_handle``には渡す関数が必要です。``is_intent_name``は関数を返しますが、リクエストが*AMAZON.CancelIntent*なのか*AMAZON.StopIntent*なのかを確認する必要があります。これを行うには、Pythonの組み込み``lambda``関数を使用して、途中に無名関数を作成します。

両方のインテントに対する応答は同じであるため、1つのハンドラーにすることで重複するコードを減らせます。

SessionEndedRequestハンドラー
~~~~~~~~~~~~~~~~~~~~~~~~

`SessionEndedRequest <https://developer.amazon.com/docs/custom-skills/request-types-reference.html#sessionendedrequest>`__\ を受け取った後は音声、カード、ディレクティブを使った応答を返すことはできませんが、クリーンアップロジックを追加するにはSessionEndedRequestHandlerが最適な場所です。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    @sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
    def session_ended_request_handler(handler_input):
        # type: (HandlerInput) -> Response
        # クリーンアップロジックをここに追加します

        return handler_input.response_builder.response

例外ハンドラーの実装
~~~~~~~~~~~~~~

以下は、catch
all例外ハンドラーをスキルに追加して、すべての例外に対してスキルが意味のあるメッセージを返すようにする例です。以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    @sb.exception_handler(can_handle_func=lambda i, e: True)
    def all_exception_handler(handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # CloudWatch Logsに例外を記録する
        print(exception)

        speech = "すみません、わかりませんでした。もう一度言ってください。"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

Lambdaハンドラーの作成
~~~~~~~~~~~~~~~~

.. note::

    カスタムスキルの場合、サービスは、AWS
    Lambdaでホスティングするか、独自のエンドポイントでウェブサービスとしてホスティングできます。

    一般的に、AWS
    Lambdaでスキルコードをホスティングするのが最も簡単です。以下のセクションでは、その方法を説明します。

    ただし、他のクラウドホスティングプロバイダーでホスティングする場合は、SDKにいくつか用意されているサポートパッケージ（``ask-sdk-webservice-support``、``flask-ask-sdk``、``django-ask-sdk``）を使用してください。このコンフィギュレーションについて詳しくは、\ `こちら <WEBSERVICE_SUPPORT.html>`__\ を参照してください。

`Lambda <https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html>`__\ ハンドラーは、AWS
Lambda関数のエントリポイントとなります。以下は、スキルが受信するすべてのリクエストのルーティングを行うLambdaハンドラー関数のコードサンプルです。Lambdaハンドラー関数は、作成したリクエストハンドラーを使用して設定されたSDKのスキルインスタンスを作成します。

以下のコードを``hello_world.py``ファイルの、前述のハンドラーの後に入力するか貼り付けます。

.. code-block:: python

    handler = sb.lambda_handler()

デコレーターを使用する場合、リクエストハンドラーと例外ハンドラーはコードの最初にインスタンス化されたスキルビルダーオブジェクトによって自動的に識別されます。

ソースコード全文
----------

hello_world.pyのソースコード全文は\ `こちら <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/docs/en/HELLO_WORLD_CODE.html>`__\ にあります。

AWS Lambda用にコードを準備する
-----------------------

コードが完成したので、Lambdaにアップロードするファイルを含む.zipファイルを作成する必要があります。

コードをAWS
Lambdaにアップロードする際に、スキルコードとその依存関係をフラットファイル構造でzipファイル内に含める必要があります。こうすると、zipでの圧縮前にコードがASK
SDK for Pythonと同じフォルダに配置されます。

.. tabs::

  .. tab:: 仮想環境でのSDKセットアップ

    仮想環境を使ってSDKをセットアップする場合、依存関係は
    仮想環境のsite-packagesフォルダにインストールされます。
    そのため、skill_envのsite-packagesフォルダに移動します。

    .. note::

      Windowsの場合、site-packagesフォルダはskill_env\Lib
      フォルダ内にあります。

    .. note::

      MacOS/Linuxの場合、site-packagesフォルダの場所は使用している
      Pythonのバージョンによって異なります。たとえば、Python
      3.6ユーザーの場合、
      skill_env/lib/Python3.6フォルダ内にsite-packagesが
      あります。

    hello_world.pyファイルをsite-packagesフォルダにコピーし、
    （そのフォルダ自体ではなく）そのフォルダのコンテンツの.zipファイルを作成します。
    ファイルに「skill.zip」という名前を付けます。`デプロイパッケージ<https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html>`__
    の作成の詳細については、
    AWS Lambdaドキュメントを参照してください。

  .. tab:: 特定のフォルダへのSDKセットアップ

    SDKを特定のフォルダにセットアップする場合、依存関係は
    その特定のフォルダにインストールされます。セットアップガイドの手順に従った場合、
    そのフォルダはskill_envです。
    hello_world.pyファイルをskill_envフォルダにコピーし、
    （そのフォルダ自体ではなく）そのフォルダのコンテンツの.zipファイルを作成します。
    ファイルに「skill.zip」という名前を付けます。`デプロイパッケージ<https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html>`__
    の作成の詳細については、
    AWS Lambdaドキュメントを参照してください。

コードをAWS Lambdaにアップロードする前に、AWS
Lambda関数を作成する必要があります。また、Alexa開発者ポータルでスキルを作成する必要があります。

AWS Lambda関数の作成
-------------------

スキルに適切なロールでAWS
Lambda関数を作成する手順については、\ `カスタムスキルをAWS Lambda関数としてホスティングする <https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html>`__ を参照してください。関数作成時には、一から作成オプションを選択し、ランタイムとして``Python
2.7``または``Python 3.6``を選択します。

AWS
Lambda関数が作成されたら、Alexaサービスでそれを呼び出すことができるようにします。これを行うには、Lambdaのコンフィギュレーションで\ **トリガー**\ タブに移動して、\ **Alexa
Skills
Kit**\ をトリガータイプとして追加します。これが完了したら、前の手順で作成したskill.zipファイルをアップロードし、ハンドラー情報とmodule_name.handlerを入力します。この例ではhello_world.handlerです。

スキルの設定とテストを行う
----------------

スキルコードをAWS
Lambdaにアップロードしたら、Alexaのスキルを設定できます。

-  以下の手順に従って新しいスキルを作成します。

   1. `Alexa Skills
      Kit開発者コンソール <https://developer.amazon.com/alexa/console/ask>`__\ にログインします。

   2. 右上の\ **スキルの作成**\ ボタンをクリックします。

   3. スキル名として「HelloWorld」と入力します。

   4. **カスタム**\ スキルを選択してから\ **スキルを作成**\ をクリックします。

-  次に、スキルの対話モデルを定義します。サイドバーの\ **呼び出し名**\ を選択し、\ **スキルの呼び出し名**\ に「ごあいさつ」を入力します。

-  次に、HelloWorldIntentというインテントを対話モデルに追加します。対話モデルのインテントセクションの下の\ **追加**\ ボタンをクリックします。「\ **カスタムインテントを作成**\ 」を選択した状態で、インテント名として「\ **HelloWorldIntent**\ 」を入力し、インテントを作成します。インテントの詳細ページで、ユーザーがこのインテントを呼び出すのに使用できるサンプル発話をいくつか追加します。この例では、以下のようなサンプル発話が適当ですが、これ以外に追加してもかまいません。

   ::

      こんにちはと言って
      ハローワールドと言って
      こんにちは
      ハイと言って
      ハイワールドと言って
      ハイ
      ごきげんいかが

-  ``AMAZON.CancelIntent``、```AMAZON.HelpIntent``、``AMAZON.StopIntent``はAlexaのビルトインインテントのため、サンプル発話を追加する必要はありません。

-  開発者コンソールでは、スキルモデル全体をJSON形式で編集できます。サイドバーで\ **JSONエディター**\ を選択します。この例では、以下のJSONスキーマを使用できます。

  .. code-block:: json

      {
        "interactionModel": {
          "languageModel": {
            "invocationName": "ごあいさつ",
            "intents": [
              {
                "name": "AMAZON.CancelIntent",
                "samples": []
              },
              {
                "name": "AMAZON.HelpIntent",
                "samples": []
              },
              {
                "name": "AMAZON.StopIntent",
                "samples": []
              },
              {
                "name": "HelloWorldIntent",
                "slots": [],
                "samples": [
                  "ごきげんいかが",
                  "ハイ",
                  "ハイワールドと言って",
                  "ハイと言って",
                  "こんにちは",
                  "ハローワールドと言って",
                  "こんにちはと言って"
                ]
              }
            ],
            "types": []
          }
        }
      }

-  対話モデルの編集が完了したら、モデルを保存してビルドします。

-  次に、スキルのエンドポイントを設定します。これを行うには次の手順に従います。

   1.  スキルの中で\ **エンドポイント**\ タブをクリックし、AWS
       LambdaのARNを選択して、作成したスキルの\ **スキルID**\ をコピーします。

   2.  新しいタブでAWS開発者コンソールを開きます。

   3.  前の手順で作成したAWS Lambda関数に移動します。

   4.  **Designer**\ メニューから、\ **Alexa Skills
       Kit**\ トリガーメニューを追加し、スクロールダウンして\ **スキルID検証**\ コンフィギュレーションにスキルIDを貼り付けます。完了したら\ **追加、保存**\ の順にクリックしてAWS
       Lambda関数を更新します。

   5.  ページ右上隅のAWS
       Lambda関数\ **ARN**\ をコピーします。ARNは一意のリソース番号です。Alexaサービスはこれを使用して、スキルの呼び出し中に必要になるAWS
       Lambda関数を識別します。

   6. Alexa Skills Kit開発者コンソールに移動して、\ **HelloWorld**\ スキルをクリックします。

   7. スキルの中で\ **エンドポイント**\ タブをクリックし、\ **AWS LambdaのARN**\ を選択して、\ **デフォルトの地域**\ にARNを貼り付けます。

   8. 残りの設定は、デフォルト値のままでかまいません。\ **エンドポイントを保存**\ をクリックします。

   9. **呼び出し名**\ タブをクリックして、モデルを保存およびビルドします。

-  この時点で、スキルをテストできるようになります。上部メニューで\ **テスト**\ をクリックします。\ **このスキルでは、テストは有効になっています**\ オプションがONになっていることを確認します。テストページを使って、テキストや音声でリクエストをシミュレーションできます。

-  呼び出し名と、サンプル発話のうちの1つを使います。たとえば、「アレクサ、あいさつして」と言うと、スキルは「こんにちは」と音声で応え、ディスプレイ付きのデバイスでは「\ *Hello
   World*\ 」カードが表示されるはずです。また、スマートフォンのAlexaアプリや\ https://alexa.amazon.com\ で\ **スキル**\ にスキルが表示されていることを確認できます。

-  さまざまなインテントや、スキルコードに対応するリクエストハンドラーを試してみてください。ひととおりのテストが完了したら、スキルの認定を申請して世界中のユーザーに公開するプロセスに進むことができます。
