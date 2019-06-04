Alexa Skills Kit SDK for Python
===============================

**ASK SDK for
Python**\ を使うと、ボイラープレートコード（毎回書かなければならないお決まりのコード）を書く手間が不要になります。これにより空いた時間をさまざまな機能の実装に充てることができ、人気のスキルをより簡単に作成できるようになります。

SDKの使用に役立つ以下のガイドをご用意しました。今後もドキュメントやサンプルを増やしていく予定です。

ガイド
-----

..  toctree::
    :caption: ガイド
    :hidden:
    :maxdepth: 2

    GETTING_STARTED
    DEVELOPING_YOUR_FIRST_SKILL
    SAMPLE_SKILLS
    SDK_SUPPORTED_ALEXA_CAPABILITIES

`ASK SDKのセットアップ <GETTING_STARTED.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pythonプロジェクトに依存関係としてSDKをインストールする方法を説明します。

`初めてのスキル開発 <DEVELOPING_YOUR_FIRST_SKILL.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hello Worldサンプルをビルドする手順を詳しく説明します。

`サンプルスキル <SAMPLE_SKILLS.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SDKを使用したスキルのサンプルです。

`SDKでサポートされているAlexaの機能 <SDK_SUPPORTED_ALEXA_CAPABILITIES.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ASK SDKでサポートされているAlexaの機能の一覧です。

SDKの機能
--------

..  toctree::
    :caption: SDKの機能
    :hidden:

    REQUEST_PROCESSING
    RESPONSE_BUILDING
    ATTRIBUTES
    SERVICE_CLIENTS
    OUT_OF_SESSION_SERVICE_CLIENTS
    SKILL_BUILDERS
    WEBSERVICE_SUPPORT


`リクエスト処理 <REQUEST_PROCESSING.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リクエストハンドラー、例外ハンドラー、リクエストと応答のインターセプターをビルドする方法を説明します。

`応答のビルド <RESPONSE_BUILDING.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ResponseBuilderを使って、テキスト、カード、オーディオといった複数の要素を使用して1つの応答を構成する方法を説明します。

`スキルのアトリビュート <ATTRIBUTES.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スキルのアトリビュートを使ったスキルデータの保存と取得の方法を説明します。

`スキルビルダー <SKILL_BUILDERS.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スキルインスタンスの構成と作成の方法を説明します。

`Alexaサービスクライアント <SERVICE_CLIENTS.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

サービスクライアントを使ってスキルからAlexa
APIにアクセスする方法を説明します。

`Alexaセッション外サービスクライアント <OUT_OF_SESSION_SERVICE_CLIENTS.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スキルのセッションコンテキスト外で機能するAlexa
APIを呼び出す方法（通常のスキルフローの外でのスキルユーザーへの通知の送信など）を説明します。

`スキルをウェブサービスとしてホスティングする <WEBSERVICE_SUPPORT.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スキルをウェブサービスとしてホスティングする方法を説明します。

.. toctree::
    :maxdepth: 1
    :caption: SDK APIリファレンス

    api

フィードバック
-------

-  バグ、機能のリクエスト、ご質問、簡単なフィードバックがあればぜひお聞かせください。新しく問題を提起する前に\ `既存の問題 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`__\ を検索してください。また、問題やプルリクエストはテンプレートに従って作成してください。プルリクエストの場合は\ `投稿のガイドライン <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`__\ に従ってください。

-  Alexaの機能に関するリクエストや投票は、\ `こちら <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`__\ をご覧ください。

そのほかのリソース
---------

.. toctree::
    :maxdepth: 2
    :caption: そのほかのリソース
    :hidden:

    SDKの問題と機能のリクエスト<https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>
    Alexa機能のリクエスト<https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>
    Alexa開発者フォーラム<https://forums.developer.amazon.com/spaces/165/index.html>

.. toctree::
    :maxdepth: 1
    :caption: そのほかの言語のASK SDK
    :hidden:

    NodeJS SDK <https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs>
    Java SDK <https://github.com/alexa/alexa-skills-kit-sdk-for-java>

コミュニティ
------

-  `Amazon開発者フォーラム <https://forums.developer.amazon.com/spaces/165/index.html>`__\ ：
   ぜひ会話に参加してください。

-  `Hackster.io <https://www.hackster.io/amazon-alexa>`__ -
   他の人がAlexaでどんなものをビルドしているか見てみましょう。

チュートリアルとガイド
-----------

-  `音声デザインガイド <https://developer.amazon.com/designing-for-voice/>`__
   ー
   会話型スキルや音声ユーザーインターフェースのデザインを学ぶことができる優れたリソースです。

-------------

指数と表
=======

* :ref:`genindex`
* :ref:`modindex`
