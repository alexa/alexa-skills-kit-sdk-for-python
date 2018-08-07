============
リクエスト処理
============

このガイドでは、スキル開発用にSDKで使用できる次のリクエスト処理コンポーネントについて説明します。

-  `ハンドラー入力 <#id2>`__
-  `リクエストハンドラー <#id3>`__
-  `例外ハンドラー <#id6>`__
-  `リクエストと応答のインターセプター <#id13>`__

ハンドラー入力
============

リクエストハンドラー、リクエストと応答のインターセプター、例外ハンドラーにはすべて、呼び出し時に共通の ``HandlerInput`` オブジェクトが渡されます。このオブジェクトには、リクエスト処理に有効な各種エンティティが含まれます。以下はその例です。

-  **request_envelope** ：スキルに送信される\ `リクエスト本文 <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#request-body-syntax>`__\ 全体を含みます。
-  **attributes_manager** ：リクエスト、セッション、永続アトリビュートへのアクセスを提供します。
-  **service_client_factory** ： Alexa APIの呼び出しが可能なサービスクライアントを構築します。
-  **response_builder** ： 応答を作成するヘルパー関数を含みます。
-  **context** ：ホストコンテナが渡すオプションのcontextオブジェクトを提供します。たとえば、AWS Lambdaで実行されるスキルの場合は、AWS Lambda関数の\ `contextオブジェクト <https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html>`__\ になります。

リクエストハンドラー
=================

リクエストハンドラーは、受信するさまざまなタイプのAlexaリクエストの処理を担当します。カスタムリクエストハンドラーを作成する方法は2つあります。

-  ``AbstractRequestHandler`` クラスを実装する。
-  `スキルビルダー <SKILL_BUILDERS.html#id1>`__\ の ``request_handler`` デコレーターを使用してカスタムハンドル関数をデコレートする。

インターフェース
--------------

AbstractRequestHandlerクラス
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AbstractRequestHandler`` クラスの使用を予定している場合は、次のメソッドを実装する必要があります。

-  **can_handle** ：``can_handle`` は、SDKによって呼び出され、指定されたハンドラーが受け取ったリクエストを処理できるかどうかを判断します。この関数は\ `ハンドラー入力 <#id2>`__\ オブジェクトを受け付け、ブール型を返すように想定されています。メソッドが\ **True**\ を返せば、ハンドラーによってリクエストが正常に処理されたと考えられます。\ **False**\ を返す場合、ハンドラーが入力リクエストを処理できず、したがって実行されず完了もしなかったと考えられます。``HandlerInput`` オブジェクトにはさまざまなアトリビュートがあるため、リクエストを正常に処理できるかどうかをSDKが判別するための任意の条件を作成できます。
-  **handle** ：``handle`` メソッドは、リクエストハンドラーを呼び出すときにSDKによって呼び出されます。この関数には、ハンドラーのリクエスト処理ロジックが含まており、\ `ハンドラー入力 <#id2>`__\ を受け取り、応答オブジェクトを返します。

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

以下は、``HelloWorldIntent`` を呼び出すことができるリクエストハンドラークラスの例です。

.. code:: python

  from ask_sdk_core.dispatch_components import AbstractRequestHandler
  from ask_sdk_model.ui import SimpleCard

  class HelloWorldIntentHandler(AbstractRequestHandler):
      def can_handle(self, handler_input):
          return handler_input.request_envelope.request.type == "IntentRequest"
            and handler_input.request_envelope.request.intent.name == "HelloWorldIntent"

      def handle(self, handler_input):
          speech_text = "Hello World";

          return handler_input.response_builder.speak(speech_text).set_card(
              SimpleCard("Hello World", speech_text)).response

``can_handle`` 関数は受け取るリクエストが ``IntentRequest`` かどうかを検出し、インテント名が ``HelloWorldIntent`` の場合にtrueを返します。``handle`` 関数は、基本的な「こんにちは」という応答を生成して返します。

SkillBuilderのrequest_handlerデコレーター
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SkillBuilderクラスの ``request_handler`` デコレーターは、``AbstractRequestHandler`` クラスに搭載されたカスタムラッパーであり、カスタムでデコレートされた任意の関数と同じ機能を提供します。ただし、デコレーターを使用するには考慮事項が2つあります。

-  デコレーターは ``can_handle_func`` パラメーターを取ります。これは ``AbstractRequestHandler`` の ``can_handle`` メソッドに似たものです。渡される値は\ `ハンドラー入力 <#id2>`__\ オブジェクトを受け付け、ブール型値を返す関数である必要があります。
-  デコレートされた関数が受け付けるパラメーターは\ `ハンドラー入力 <#id2>`__\ 1つのみであり、``Response`` オブジェクトを返します。

.. code:: python

    class SkillBuilder(object):
        ....
        def request_handler(self, can_handle_func):
            def wrapper(handle_func):
                # wrap the can_handle and handle into a class
                # add the class into request handlers list
                ....
            return wrapper

以下は、``HelloWorldIntent`` を処理できるリクエストハンドラー関数の例です。

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

``is_intent_name`` 関数はstringパラメーターを受け取り無名関数を返します。この無名関数は、``HandlerInput`` を入力パラメーターとして受け取って、``HandlerInput`` の受信リクエストが ``IntentRequest`` であるかを確認し、インテント名が ``string`` に渡されているものであればそれを返します。この例では ``HelloWorldIntent`` です。``handle`` 関数は、基本的な「こんにちは」という応答を生成して返します。

リクエストハンドラーの登録と処理
---------------------------

SDKは、リクエストハンドラーで、スキルビルダーに指定された順序で ``can_handle`` 関数を呼び出します。

``AbstractRequestHandler`` クラスを使用する方法に従っている場合、次の方法でリクエストハンドラーを登録できます

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # Implement FooHandler, BarHandler, BazHandler classes

    sb.request_handlers.extend([
            FooHandler(),
            BarHandler(),
            BazHandler()])

``request_handler`` デコレーターを使用する方法に従っている場合、ハンドラー関数を明示的に登録する必要はありません。スキルビルダーインスタンスを使用してすでにデコレートされています。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # decorate foo_handler, bar_handler, baz_handler functions

上記の例では、SDKが以下の順序でリクエストハンドラーを呼び出します。

1. ``FooHandler`` クラス ／ ``foo_handler`` 関数
2. ``BarHandler`` クラス ／ ``bar_handler`` 関数
3. ``BazHandle`` rクラス ／ ``baz_handler`` 関数

SDKは、指定されたリクエストを処理できる最初のハンドラーを常に選択します。この例では、``FooHandler`` クラス ／ ``foo_handler`` 関数および ``BarHandler``クラス ／ ``bar_handler`` 関数のどちらも指定のリクエストを処理できる場合、``FooHandler`` クラス／``foo_handler`` 関数が常に呼び出されます。リクエストハンドラーのデザインや登録を行う際には、この点を考慮に入れてください。

例外ハンドラー
============

例外ハンドラーはリクエストハンドラーに似ていますが、リクエストではなく1つまたは複数のタイプの例外を処理します。リクエストの処理中に未処理の例外がスローされると、SDKが例外ハンドラーを呼び出します。

ハンドラーは\ `ハンドラー入力 <#id2>`__\ オブジェクトに加えて、入力リクエストの処理中に発生した例外にもアクセスできます。そのため、ハンドラーが該当する例外の処理方法を判別しやすくなります。

`リクエストハンドラー <#id3>`__\ と同様に、カスタムリクエストインターセプターも2通りの方法で実装できます。

-  ``AbstractExceptionHandler`` クラスを実装する。
-  `スキルビルダー <SKILL_BUILDERS.html#id1>`__\ の ``exception_handler`` デコレーターを使用してカスタム例外ハンドル関数をデコレートする。

インターフェース
--------------

AbstractExceptionHandlerクラス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AbstractExceptionHandler`` クラスの使用を予定している場合は、次のメソッドを実装する必要があります。

-  **can_handle** ：``can_handle`` メソッドはSDKによって呼び出され、指定されたハンドラーが例外を処理できるかどうかを判断します。ハンドラーが例外を処理できる場合は\ **True**\ 、できない場合は\ **False**\ を返します。catch-allハンドラーを作成する場合は常に ``True`` を返します。
-  **handle** ：``handle`` メソッドは例外ハンドラーを呼び出すときにSDKによって呼び出されます。この関数には、例外処理ロジックがすべて含まれ、応答オブジェクトを返します。

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

以下は、名前に「AskSdk」が含まれる例外をすべて処理する例外ハンドラーの例です。

.. code:: python

   class AskExceptionHandler(AbstractExceptionHandler):
        def can_handle(self, handler_input, exception):
            return 'AskSdk' in exception.__class__.__name__

        def handle(self, handler_input, exception):
            speech_text = "Sorry, I am unable to figure out what to do. Try again later!!";

            return handler_input.response_builder.speak(speech_text).response

ハンドラーの ``can_handle`` メソッドは、受け取る例外の名前が「AskSdk」で始まる場合にTrueを返します。``handle`` メソッドは、ユーザーに正常な例外応答を返します。

SkillBuilderのexception_handlerデコレーター
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SkillBuilderクラスの ``exception_handler`` デコレーターは、``AbstractExceptionHandler`` クラスに搭載されたカスタムラッパーであり、カスタムでデコレートされた任意の関数と同じ機能を提供します。ただし、デコレーターを使用するには以下の2点を考慮してください。

-  デコレーターは ``can_handle_func`` パラメーターを取ります。これは ``AbstractExceptionHandler`` の ``can_handle`` メソッドに似たものです。渡される値は\ `ハンドラー入力 <#id2>`__\ オブジェクトを例外インスタンスとして受け付け、ブール型値を返す関数である必要があります。
-  デコレートされた関数が受け付けるパラメーターは\ `ハンドラー入力 <#id2>`__\ オブジェクトおよび例外オブジェクトの2つのみです。応答オブジェクトが返されます。

.. code:: python

    class SkillBuilder(object):
        ....
        def exception_handler(self, can_handle_func):
            def wrapper(handle_func):
                # wrap the can_handle and handle into a class
                # add the class into exception handlers list
                ....
            return wrapper

以下は、名前に「AskSdk」が含まれる例外をすべて処理する例外ハンドラー関数の例です。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    @sb.exception_handler(can_handle_func = lambda input, e: 'AskSdk' in e.__class__.__name__)
    def ask_exception_intent_handler(handler_input, exception):
        speech_text = "Sorry, I am unable to figure out what to do. Try again later!!";

        return handler_input.response_builder.speak(speech_text).response


例外ハンドラーの登録と処理
-----------------------

``AbstractExceptionHandler`` クラスを使用する方法に従っている場合、次の方法でリクエストハンドラーを登録できます

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # Implement FooExceptionHandler, BarExceptionHandler, BazExceptionHandler classes

    sb.add_exception_handler(FooExceptionHandler())
    sb.add_exception_handler(BarExceptionHandler())
    sb.add_exception_handler(BazExceptionHandler())

``exception_handler`` デコレーターを使用する方法に従っている場合、ハンドラー関数を明示的に登録する必要はありません。スキルビルダーインスタンスを使用してすでにデコレートされています。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # decorate foo_exception_handler, bar_exception_handler, baz_exception_handler functions


リクエストハンドラーと同様に、例外ハンドラーはスキルで指定した順序で実行されます。

リクエストと応答のインターセプター
=============================

SDKは、一致する ``RequestHandler`` の\ **実行前**\ と\ **実行後**\ に実行するリクエストと応答のグローバルインターセプターをサポートします。

リクエストインターセプター
-----------------------

グローバルリクエストインターセプターは、登録されたリクエストハンドラーの処理前に、\ `ハンドラー入力 <handler-input>`__\ オブジェクトを受け付けて処理します。\ `リクエストハンドラー <#id3>`__\ と同様に、カスタムリクエストインターセプターも2通りの方法で実装できます。

-  ``AbstractRequestInterceptor`` クラスを実装する。

-  `スキルビルダー <SKILL_BUILDERS.html#id1>`__\ の ``global_request_interceptor`` デコレーターを使用してカスタム処理関数をデコレートする。

インターフェース
~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AbstractRequestInterceptorクラス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AbstractRequestInterceptor`` クラスを使用するには、処理メソッドを実装する必要があります。このメソッドは\ `ハンドラー入力 <#id2>`__\ インスタンスを取得し、何も返しません。

.. code:: python

    class AbstractRequestInterceptor(object):
        @abstractmethod
        def process(self, handler_input):
            # type: (HandlerInput) -> None
            pass

以下は、Alexaサービスが受け取ったリクエストを、処理の前にAWS CloudWatchログに書き込むリクエストインターセプタークラスの例です。

.. code:: python

  from ask_sdk_core.dispatch_components import AbstractRequestInterceptor

  class LoggingRequestInterceptor(AbstractRequestInterceptor):
      def process(self, handler_input):
          print("Request received: {}".format(handler_input.request_envelope.request))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SkillBuilderのglobal_request_interceptorデコレーター
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SkillBuilderクラスの ``global_request_interceptor`` デコレーターは、``AbstractRequestInterceptor`` クラスに搭載されたカスタムラッパーであり、カスタムでデコレートされた任意の関数と同じ機能を提供します。ただし、デコレーターを使用するには以下の2点を考慮してください。

-  デコレーターはスキルビルダーインスタンスを必要とするため、インターセプターを登録するには、関数名としてではなく関数として呼び出される必要があります。
-  デコレートされた関数が受け付けるパラメーターは\ `ハンドラー入力 <#id2>`__\ オブジェクト1つのみであり、関数からの戻り値はキャプチャーされません。

.. code:: python

    class SkillBuilder(object):
        ....
        def global_request_interceptor(self):
            def wrapper(process_func):
                # wrap the process_func into a class
                # add the class into request interceptors list
                ....
            return wrapper

以下は、リクエストインターセプターとして使用できるログ記録関数の例です。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    @sb.global_request_interceptor()
    def request_logger(handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


リクエストインターセプターの登録と処理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リクエストのインターセプターは、リクエストハンドラーが受け取ったリクエストを処理する直前に呼び出されます。\ `ハンドラー入力 <#id2>`__\ のアトリビュートマネージャー内のリクエストアトリビュートは、リクエストインターセプターが他のリクエストインターセプターやリクエストハンドラーにデータやエンティティを渡す方法を提供します。

``AbstractRequestInterceptor`` クラスを使用する方法に従っている場合、次の方法でリクエストインターセプターを登録できます

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # Implement FooInterceptor, BarInterceptor, BazInterceptor classes

    sb.add_global_request_interceptor(FooInterceptor())
    sb.add_global_request_interceptor(BarInterceptor())
    sb.add_global_request_interceptor(BazInterceptor())

``global_request_interceptor`` デコレーターを使用する方法に従っている場合、インターセプター関数を明示的に登録する必要はありません。スキルビルダーインスタンスを使用してすでにデコレートされています。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # decorate foo_interceptor, bar_interceptor, baz_interceptor functions

上記の例では、SDKが以下の順序ですべてのリクエストインターセプターを実行します。

1. ``FooInterceptor`` クラス ／ ``foo_interceptor`` 関数
2. ``BarInterceptor`` クラス ／ ``bar_interceptor`` 関数
3. ``BazInterceptor`` クラス ／ ``baz_interceptor`` 関数

応答インターセプター
-----------------

グローバル応答インターセプターは、サポートされるリクエストハンドラーの処理後に、\ `ハンドラー入力 <#id2>`__\ オブジェクト、つまり応答を受け付けて処理します。\ `リクエストインターセプター <#id10>`__\ と同様に、カスタム応答インターセプターも二通りの方法で実装できます。

-  ``AbstractResponseInterceptor`` クラスを実装する。
-  `スキルビルダー <SKILL_BUILDERS.html#id1>`__\ の ``global_response_interceptor`` デコレーターを使用してカスタム処理関数をデコレートする。

インターフェース
~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AbstractResponseInterceptorクラス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AbstractResponseInterceptor`` クラスを使用するには、処理メソッドを実装する必要があります。このメソッドは\ `ハンドラー入力 <#id2>`__\ インスタンスの、先に実行されたリクエストハンドラーから返された応答オブジェクトを取ります。このメソッドから返されるものはありません。

.. code:: python

    class AbstractResponseInterceptor(object):
        @abstractmethod
        def process(self, handler_input, response):
            # type: (HandlerInput, Response) -> None
            pass

以下は、正常に処理されたリクエストから受け取った応答を、Alexaサービスにその応答が返される前にAWS CloudWatchログに書き込むレスポンスインターセプタークラスの例です。

.. code:: python

  from ask_sdk_core.dispatch_components import AbstractResponseInterceptor

  class LoggingResponseInterceptor(AbstractResponseInterceptor):
      def process(handler_input, response):
          print("Response generated: {}".format(response))


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SkillBuilderのglobal_response_interceptorデコレーター
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SkillBuilderクラスの ``global_response_interceptor`` デコレーターは、``AbstractResponseInterceptor`` クラスに搭載されたカスタムラッパーであり、カスタムでデコレートされた任意の関数と同じ機能を提供します。ただし、デコレーターを使用するには以下の2点を考慮してください。

-  デコレーターはスキルビルダーインスタンスを必要とするため、インターセプターを登録するには、関数名としてではなく関数として呼び出される必要があります。
-  デコレートされた関数は2つのパラメーターを受け付けます。それぞれ\ `ハンドラー入力 <#id2>`__\ オブジェクトおよび応答オブジェクトです。この関数から返される値はキャプチャーされません。

.. code:: python

    class SkillBuilder(object):
        ....
        def global_response_interceptor(self):
            def wrapper(process_func):
                # wrap the process_func into a class
                # add the class into response interceptors list
                ....
            return wrapper

以下は、応答インターセプターとして使用できるログ記録関数の例です。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    @sb.global_response_interceptor()
    def response_logger(handler_input, response):
        print("Response generated: {}".format(response))


応答インターセプターの登録と処理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

応答インターセプターは、受け取るリクエストのリクエストハンドラーが実行された直後に呼び出されます。

``AbstractResponseInterceptor`` クラスを使用する方法に従っている場合、次の方法で応答インターセプターを登録できます

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # Implement FooInterceptor, BarInterceptor, BazInterceptor classes

    sb.add_global_response_interceptor(FooInterceptor())
    sb.add_global_response_interceptor(BarInterceptor())
    sb.add_global_response_interceptor(BazInterceptor())

``global_response_interceptor`` デコレーターを使用する方法に従っている場合、インターセプター関数を明示的に登録する必要はありません。スキルビルダーインスタンスを使用してすでにデコレートされています。

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder

    sb = SkillBuilder()

    # decorate foo_interceptor, bar_interceptor, baz_interceptor functions

`リクエストインターセプター <#id12>`__\ の処理と同様に、応答インターセプターはすべて、登録順に実行されます。
