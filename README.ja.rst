ASK SDK for Python
===============================
`English <README.rst>`_ |  `日本語 <README.ja.rst>`_

|Build Status| |Japanese Docs| |License|

**ASK SDK for Python**\ を使うと、ボイラープレートコード（毎回書かなければならないお決まりのコード）を書く手間が不要になります。これにより空いた時間をさまざまな機能の実装に充てることができ、人気のスキルをより簡単に作成できるようになります。

.. |Build Status| image:: https://img.shields.io/travis/alexa-labs/alexa-skills-kit-sdk-for-python/master.svg?style=flat
    :target: https://travis-ci.org/alexa-labs/alexa-skills-kit-sdk-for-python
    :alt: Build Status
.. |Docs| image:: https://img.shields.io/readthedocs/alexa-skills-kit-python-sdk.svg?style=flat
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io
    :alt: Read the docs
.. |Runtime Version| image:: http://img.shields.io/pypi/v/ask-sdk-runtime.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-runtime/
    :alt: Version
.. |Runtime Downloads| image:: https://pepy.tech/badge/ask-sdk-runtime
    :target: https://pepy.tech/project/ask-sdk-runtime
    :alt: Downloads
.. |Core Version| image:: http://img.shields.io/pypi/v/ask-sdk-core.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-core/
    :alt: Version
.. |Core Downloads| image:: https://pepy.tech/badge/ask-sdk-core
    :target: https://pepy.tech/project/ask-sdk-core
    :alt: Downloads
.. |DynamoDb Version| image:: http://img.shields.io/pypi/v/ask-sdk-dynamodb-persistence-adapter.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-dynamodb-persistence-adapter/
    :alt: Version
.. |DynamoDb Downloads| image:: https://pepy.tech/badge/ask-sdk-dynamodb-persistence-adapter
    :target: https://pepy.tech/project/ask-sdk-dynamodb-persistence-adapter
    :alt: Downloads
.. |Standard Version| image:: http://img.shields.io/pypi/v/ask-sdk.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk/
    :alt: Version
.. |Standard Downloads| image:: https://pepy.tech/badge/ask-sdk
    :target: https://pepy.tech/project/ask-sdk
    :alt: Downloads
.. |Webservice Version| image:: http://img.shields.io/pypi/v/ask-sdk-webservice-support.svg?style=flat
    :target: https://pypi.python.org/pypi/ask-sdk-webservice-support/
    :alt: Version
.. |Webservice Downloads| image:: https://pepy.tech/badge/ask-sdk-webservice-support
    :target: https://pepy.tech/project/ask-sdk-webservice-support
    :alt: Downloads
.. |Flask Sdk Version| image:: http://img.shields.io/pypi/v/flask-ask-sdk.svg?style=flat
    :target: https://pypi.python.org/pypi/flask-ask-sdk/
    :alt: Version
.. |Flask Sdk Downloads| image:: https://pepy.tech/badge/flask-ask-sdk
    :target: https://pepy.tech/project/flask-ask-sdk
    :alt: Downloads
.. |Django Sdk Version| image:: http://img.shields.io/pypi/v/django-ask-sdk.svg?style=flat
    :target: https://pypi.python.org/pypi/django-ask-sdk/
    :alt: Version
.. |Django Sdk Downloads| image:: https://pepy.tech/badge/django-ask-sdk
    :target: https://pepy.tech/project/django-ask-sdk
    :alt: Downloads
.. |License| image:: http://img.shields.io/pypi/l/ask-sdk-core.svg?style=flat
    :target: https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/LICENSE
    :alt: License

Package Versions
----------------
====================================   ==================
Package                                Version
------------------------------------   ------------------
ask-sdk-runtime                        |Runtime Version| |Runtime Downloads|
ask-sdk-core                           |Core Version| |Core Downloads|
ask-sdk-dynamodb-persistence-adapter   |DynamoDb Version| |DynamoDb Downloads|
ask-sdk                                |Standard Version| |Standard Downloads|
ask-sdk-webservice-support (Beta)      |Webservice Version| |Webservice Downloads|
flask-ask-sdk (Beta)                   |Flask Sdk Version| |Flask Sdk Downloads|
django-ask-sdk (Beta)                  |Django Sdk Version| |Django Sdk Downloads|
====================================   ==================


SDKの使用をより迅速に開始するには、次のリソースを参照してください。

技術文書
-------

========================================================================== ======
Language                                                                   Docs
========================================================================== ======
`English <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/>`_ |English Docs|
`日本語 <https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/>`_   |Japanese Docs|
========================================================================== ======

.. |English Docs| image:: https://readthedocs.org/projects/alexa-skills-kit-python-sdk/badge/?version=latest
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/?badge=latest
    :alt: Read the docs english

.. |Japanese Docs| image:: https://readthedocs.org/projects/alexa-skills-kit-python-sdk-japanese/badge/?version=latest
    :target: https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/?badge=latest
    :alt: Read the docs japanese

モデル
------

SDKはネイティブのAlexa JSONリクエストおよびレスポンスではなく、モデルクラスで動作します。これらのモデルクラスは、 `開発者向けドキュメント <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html>` __のRequest、Response JSONスキーマを使用して生成されます。モデルクラスのソースコードは `ここに <https://github.com/alexa/alexa-apis-for-python>` __にあります。

モデルクラスのドキュメントは `here <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/models/ask_sdk_model.html>` __にあります。

サンプル
----

`Hello Worldスキルサンプル <https://github.com/alexa/skill-sample-python-helloworld-classes>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このコードサンプルでは、サンプルがトリガーされたときのAlexaの応答を聞くことができます。Alexa
Skills KitやAWS Lambdaに慣れるための最小限のサンプルです。

`カラーピッカースキルサンプル <https://github.com/alexa/skill-sample-python-colorpicker>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hello
Worldから機能を一歩進めて、ユーザーからの入力をキャプチャーできるようにします。スロットの使い方についても説明します。さらに、セッションアトリビュートと、リクエスト、応答のインターセプターの使い方も説明します。

`ハイ＆ローゲームスキルサンプル <https://github.com/alexa/skill-sample-python-highlowgame>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

基本的なハイ＆ローゲームスキルのテンプレートです。ユーザーが数字を推測し、Alexaがその数字が正解より大きいか小さいかを答えます。

`デバイスアドレスAPIスキルサンプル <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/samples/GetDeviceAddress>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ユーザーのデバイス設定で設定したアドレスをリクエストし、設定されたアドレスにアクセスするサンプルスキルです。


より多くのサンプルについては、 `samples <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SAMPLE_SKILLS.html>`_ セクションを見てください。

------------

フィードバック
-------

-  バグ、機能のリクエスト、ご質問、簡単なフィードバックがあればぜひお聞かせください。新しく問題を提起する前に\ `既存の問題 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`__\ を検索してください。また、問題やプルリクエストはテンプレートに従って作成してください。プルリクエストの場合は\ `投稿のガイドライン <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`__\ に従ってください。

-  Alexaの機能に関するリクエストや投票は、\ `こちら <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`__\ をご覧ください。

その他のリソース
--------------

その他の言語AlexaスキルキットSDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <embed>
        <div>
            <p><a href="https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs"><img src="https://github.com/konpa/devicon/blob/master/icons/nodejs/nodejs-original.svg?sanitize=true" width="25px" /> NodeJS用のAlexaスキルキットSDK</a></p>
            <p><a href="https://github.com/amzn/alexa-skills-kit-java"><img src="https://github.com/konpa/devicon/raw/master/icons/java/java-original.svg?sanitize=true" width="25px" /> AlexaスキルキットSDK for Java</a></p>
        </div>
    </embed>

コミュニティ
~~~~~~

-  `Amazon開発者フォーラム <https://forums.developer.amazon.com/spaces/165/index.html>`__\ ：
   ぜひ会話に参加してください。

-  `Hackster.io <https://www.hackster.io/amazon-alexa>`__ ー
   他の人がAlexaでどんなものをビルドしているか見てみましょう。

チュートリアルとガイド
~~~~~~~~~~~

-  `音声デザインガイド <https://developer.amazon.com/designing-for-voice/>`__
   ー
   会話型スキルや音声ユーザーインターフェースのデザインを学ぶことができる優れたリソースです。

