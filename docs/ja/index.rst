ASK SDK for Python（ベータ版）
===============================

**ASK SDK for
Python（ベータ版）**\ を使うと、ボイラープレートコード（毎回書かなければならないお決まりのコード）を書く手間が不要になります。これにより空いた時間をさまざまな機能の実装に充てることができ、人気のスキルをより簡単に作成できるようになります。

SDKの使用に役立つ以下のガイドをご用意しました。今後もドキュメントやサンプルを増やしていく予定です。

ガイド
-----

..  toctree::
    :caption: ガイド
    :hidden:
    :maxdepth: 2

    GETTING_STARTED
    DEVELOPING_YOUR_FIRST_SKILL
    <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SAMPLE_SKILLS.html>

`ASK SDKのセットアップ <GETTING_STARTED.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pythonプロジェクトに依存関係としてSDKをインストールする方法を説明します。

`初めてのスキル開発 <DEVELOPING_YOUR_FIRST_SKILL.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hello Worldサンプルをビルドする手順を詳しく説明します。

SDKの機能
--------

..  toctree::
    :caption: SDKの機能
    :hidden:

    REQUEST_PROCESSING
    ATTRIBUTES
    RESPONSE_BUILDING
    SERVICE_CLIENTS
    SKILL_BUILDERS

`リクエスト処理 <REQUEST_PROCESSING.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リクエストハンドラー、例外ハンドラー、リクエストと応答のインターセプターをビルドする方法を説明します。

`スキルのアトリビュート <ATTRIBUTES.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スキルのアトリビュートを使ったスキルデータの保存と取得の方法を説明します。

`応答のビルド <RESPONSE_BUILDING.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ResponseBuilderを使って、テキスト、カード、オーディオといった複数の要素を使用して1つの応答を構成する方法を説明します。

`Alexaサービスクライアント <SERVICE_CLIENTS.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

サービスクライアントを使ってスキルからAlexa
APIにアクセスする方法を説明します。

`スキルビルダー <SKILL_BUILDERS.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スキルインスタンスの構成と作成の方法を説明します。

---------


サンプル
----

`Hello Worldスキルサンプル <https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/blob/master/samples/HelloWorld>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このコードサンプルでは、サンプルがトリガーされたときのAlexaの応答を聞くことができます。Alexa
Skills KitやAWS Lambdaに慣れるための最小限のサンプルです。

`カラーピッカースキルサンプル <https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/blob/master/samples/ColorPicker>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hello
Worldから機能を一歩進めて、ユーザーからの入力をキャプチャーできるようにします。スロットの使い方についても説明します。さらに、セッションアトリビュートと、リクエスト、応答のインターセプターの使い方も説明します。

`ハイ＆ローゲームスキルサンプル <https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/blob/master/samples/HighLowGame>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

基本的なハイ＆ローゲームスキルのテンプレートです。ユーザーが数字を推測し、Alexaがその数字が正解より大きいか小さいかを答えます。

`デバイスアドレスAPIスキルサンプル <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/samples/GetDeviceAddress>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ユーザーのデバイス設定で設定したアドレスをリクエストし、設定されたアドレスにアクセスするサンプルスキルです。

------------

.. toctree::
   :maxdepth: 1
   :caption: APIリファレンス
   :hidden:

   api

`APIリファレンス <api.html>`__
-----------------------------
SDK APIおよびSDKモデルのリファレンス

------------

フィードバック
-------

-  バグ、機能のリクエスト、ご質問、簡単なフィードバックがあればぜひお聞かせください。新しく問題を提起する前に\ `既存の問題 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>`__\ を検索してください。また、問題やプルリクエストはテンプレートに従って作成してください。プルリクエストの場合は\ `投稿のガイドライン <https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/CONTRIBUTING.md>`__\ に従ってください。

-  Alexaの機能に関するリクエストや投票は、\ `こちら <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>`__\ をご覧ください。

その他のリソース
--------------

.. toctree::
   :maxdepth: 2
   :caption: Additional Resources
   :hidden:

   SDK Issues and feature requests <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues>
   Alexa feature requests <https://alexa.uservoice.com/forums/906892-alexa-skills-developer-voice-and-vote>
   Alexa Developer Forums <https://forums.developer.amazon.com/spaces/165/index.html>

.. toctree::
   :maxdepth: 1
   :caption: Other language ASK SDKs
   :hidden:

   NodeJS SDK <https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs>
   Java SDK <https://github.com/alexa/alexa-skills-kit-sdk-for-java>

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

------------

指数と表
=======

* :ref:`genindex`
* :ref:`modindex`