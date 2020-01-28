ASK SDK for Python
===============================
`English <README.rst>`_ |  `日本語 <README.ja.rst>`_

|Build Status| |Japanese Docs| |License|

**ASK SDK for Python**\ を使うと、ボイラープレートコード（毎回書かなければならないお決まりのコード）を書く手間が不要になります。これにより空いた時間をさまざまな機能の実装に充てることができ、人気のスキルをより簡単に作成できるようになります。

.. |Build Status| image:: https://img.shields.io/travis/alexa/alexa-skills-kit-sdk-for-python/master.svg?style=flat
    :target: https://travis-ci.org/alexa/alexa-skills-kit-sdk-for-python
    :alt: Build Status
.. |Docs|
    :target: https://developer.amazon.com/docs/alexa-skills-kit-sdk-for-python/overview.html
    :alt: Technical documentation
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
ask-sdk-webservice-support             |Webservice Version| |Webservice Downloads|
flask-ask-sdk                          |Flask Sdk Version| |Flask Sdk Downloads|
django-ask-sdk                         |Django Sdk Version| |Django Sdk Downloads|
====================================   ==================


SDKの使用をより迅速に開始するには、次のリソースを参照してください。

技術文書
-------

- `English <https://developer.amazon.com/docs/alexa-skills-kit-sdk-for-python/overview.html>`__
- `日本語 <https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/>`__

モデル
------

SDKはネイティブのAlexa JSONリクエストおよびレスポンスではなく、モデルクラスで動作します。これらのモデルクラスは、 `開発者向けドキュメント <https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html>` __のRequest、Response JSONスキーマを使用して生成されます。モデルクラスのソースコードは `ここに <https://github.com/alexa/alexa-apis-for-python>` __にあります。

モデルクラスのドキュメントは `here <https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/models/ask_sdk_model.html>` __にあります。

サンプル
----

このセクションでは、ASK SDK for
Pythonを使って魅力的なAlexaスキルを開発する方法を説明するスキルサンプルを紹介します。

`Hello World（クラス使用） <https://github.com/alexa/skill-sample-python-helloworld-classes>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このコードサンプルでは、サンプルがトリガーされたときのAlexaの応答を聞くことができます。Alexa
Skills KitやAWS
Lambdaに慣れるための最小限のサンプルです。このサンプルでは、リクエストハンドラーのクラスを使用してスキルを作成する方法を説明します。詳細については、 `リクエスト処理 <REQUEST_PROCESSING.html>`__ を参照してください。

`Hello World（デコレーター使用） <https://github.com/alexa/skill-sample-python-helloworld-decorators>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このコードサンプルでは、サンプルがトリガーされたときのAlexaの応答を聞くことができます。Alexa
Skills KitやAWS
Lambdaに慣れるための最小限のサンプルです。このサンプルでは、リクエストハンドラーのデコレーターを使用してスキルを作成する方法を説明します。詳細については、 `リクエスト処理 <REQUEST_PROCESSING.html>`__ を参照してください。

`カラーピッカー <https://github.com/alexa/skill-sample-python-colorpicker>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hello
Worldから機能を一歩進めて、ユーザーが好きな色を指定したら、Alexaが覚えてユーザーに知らせるようにします。ユーザーからの入力をキャプチャーできるようにします。スロットの使い方についても説明します。さらに、セッションアトリビュートと、リクエスト、応答のインターセプターの使い方も説明します。

`ファクト <https://github.com/alexa/skill-sample-python-fact>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

基本的な豆知識スキルのテンプレートです。トピックについての豆知識のリストを提供すると、ユーザーがスキルを呼び出したときに、Alexaがリストから豆知識をランダムに選んでユーザーに伝えます。スキルで複数のロケールを使用し国際化する方法を説明します。

`クイズゲーム <https://github.com/alexa/skill-sample-python-quiz-game>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

基本的なクイズゲームスキルのテンプレートです。あらかじめ提供しておいた豆知識のリストの中から、Alexaがユーザーにクイズを出します。画面付きのAlexa搭載デバイスでの表示をサポートする、テンプレートレンダリングディレクティブの使い方について説明します。

`デバイスのアドレス <https://github.com/alexa/alexa-skills-kit-sdk-for-python/tree/master/samples/GetDeviceAddress>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ユーザーのデバイス設定で設定したアドレスをリクエストし、設定されたアドレスにアクセスするサンプルスキルです。SDKを使用したAlexa
APIの使い方について説明します。詳細については、\ `Alexaサービスクライアント <SERVICE_CLIENTS.html>`__\ を参照してください。

`スキル内課金を使用した豆知識 <https://github.com/alexa/skill-sample-python-fact-in-skill-purchases>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`スキル内課金 <https://developer.amazon.com/docs/in-skill-purchase/isp-overview.html>`__ 機能を使用した豆知識スキルのサンプルです。購入を促進するさまざまなパックや、パックを一括でロック解除するサブスクリプションを提供します。収益化Alexaサービスの呼び出し方とASK
CLIを使ってスキル内課金を有効にする方法を説明します。

`シティガイド <https://github.com/alexa/skill-sample-python-city-guide>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

周辺地域のお勧め情報スキルのテンプレートです。Alexaはユーザーのリクエストに従って、開発者が提供したデータからお勧め情報をユーザーに知らせます。スキルから外部APIを呼び出す方法を説明します。

`ペットマッチ <https://github.com/alexa/skill-sample-python-petmatch>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ユーザーとペットをマッチングするサンプルスキルです。Alexaは一致するペットを見つけるのに必要な情報をユーザーにたずねます。必要な情報をすべて収集できたら、スキルはデータを外部のウェブサービスに送信し、そこでデータが処理されてマッチングデータが返されます。ダイアログ管理と `エンティティ解決 <https://developer.amazon.com/docs/custom-skills/define-synonyms-and-ids-for-slot-type-values-entity-resolution.html>`__ を使って、プロンプトを出してユーザーから複数の値を受け取り解析する方法を説明します。

`ハイ＆ローゲーム <https://github.com/alexa/skill-sample-python-highlowgame>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

基本的なハイ＆ローゲームスキルのテンプレートです。ユーザーが数字を推測し、Alexaがその数字が正解より大きいか小さいかを答えます。SDKの永続アトリビュートと永続アダプターの使い方について説明します。

`AudioPlayer SingleStreamおよびMultiStream <https://github.com/alexa/skill-sample-python-audio-player>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alexaの `AudioPlayerインターフェース <https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-audioplayer-interface-reference>`__ と `PlaybackControllerインターフェース <https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-playbackcontroller-interface-reference>`__ を使ってAudioPlayerスキルを開発する方法を説明するスキルサンプルです。SingleStreamスキルサンプルでは、ローカリゼーションのサポート付きでライブラジオスキルを作成する方法を説明します。MultiStreamスキルサンプルでは、録音済みの複数のオーディオストリームを再生できる基本的なポッドキャストスキルを作成する方法を説明します。

`Pager Karaoke <https://github.com/alexa-labs/skill-sample-python-pager-karaoke>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このサンプルでは、APLの3つの機能である `Pagerコンポーネント <https://developer.amazon.com/docs/alexa-presentation-language/apl-pager.html>`__ 、 `SpeakItemコマンド <https://developer.amazon.com/docs/alexa-presentation-language/apl-standard-commands.html#speakitem-command>`__ 、スキルコードの `デバイスの特性 <https://developer.amazon.com/docs/alexa-presentation-language/apl-viewport-characteristics.html>`__ へのアクセスについて説明します。

------------

SDKでサポートされているAlexaの機能
=======================

このセクションでは、現在SDKでサポートされているAlexaのすべての機能を紹介します。

正式版
------

-  `Amazon Pay <https://developer.amazon.com/docs/amazon-pay/integrate-skill-with-amazon-pay.html>`__

-  `Audio Player <https://developer.amazon.com/docs/custom-skills/audioplayer-interface-reference.html>`__

-  `Display – 画面付きデバイス用のBodyテンプレート <https://developer.amazon.com/docs/custom-skills/create-skills-for-alexa-enabled-devices-with-a-screen.html>`__

-  `GadgetsGame Engine – Echo Buttons（日本未対応） <https://developer.amazon.com/docs/custom-skills/game-engine-interface-reference.html>`__

-  `Directiveサービス（プログレッシブ応答） <https://developer.amazon.com/docs/custom-skills/send-the-user-a-progressive-response.html>`__

-  `メッセージ <https://developer.amazon.com/docs/smapi/send-a-message-request-to-a-skill.html>`__

-  `収益化 <https://developer.amazon.com/alexa-skills-kit/make-money>`__

-  `ビデオ <https://developer.amazon.com/docs/custom-skills/videoapp-interface-reference.html>`__

-  `デバイスのアドレス <https://developer.amazon.com/docs/custom-skills/device-address-api.html>`__

-  `リスト <https://developer.amazon.com/docs/custom-skills/access-the-alexa-shopping-and-to-do-lists.html#alexa-lists-access>`__

-  `ユーザー連絡先情報のリクエスト <https://developer.amazon.com/docs/alexa/custom-skills/request-customer-contact-information-for-use-in-your-skill.html>`__

-  `ユーザー設定情報の取得 <https://developer.amazon.com/docs/smapi/alexa-settings-api-reference.html>`__

-  `アカウントリンク <https://developer.amazon.com/docs/account-linking/understand-account-linking.html>`__

-  `スロットタイプ値の同義語とIDを定義する（エンティティ解決） <https://developer.amazon.com/docs/custom-skills/define-synonyms-and-ids-for-slot-type-values-entity-resolution.html>`__

-  `ダイアログ管理 <https://developer.amazon.com/docs/custom-skills/dialog-interface-reference.html>`__

-  `位置情報サービス <https://developer.amazon.com/docs/custom-skills/location-services-for-alexa-skills.html>`__

-  `リマインダー <https://developer.amazon.com/docs/smapi/alexa-reminders-overview.html>`__

-  `プロアクティブイベント <https://developer.amazon.com/docs/smapi/proactive-events-api.html>`__

-  `動的エンティティ <https://developer.amazon.com/docs/custom-skills/use-dynamic-entities-for-customized-interactions.html>`__

-  `スキルメッセージ <https://developer.amazon.com/docs/smapi/skill-messaging-api-reference.html>`__

-  `Connections <https://developer.amazon.com/blogs/alexa/post/7b332b32-893e-4cad-be07-a5877efcbbb4/skill-connections-preview-now-skills-can-work-together-to-help-customers-get-more-done>`__
プレビュー版
-------

..警告::

    以下の機能は、プレビュー版としてリリースされています。インターフェースは正式版リリースの際に変更される可能性があります。

-  `Alexa Presentation Language <https://developer.amazon.com/docs/alexa-presentation-language/apl-overview.html>`__

-  `無指名対話 <https://developer.amazon.com/docs/custom-skills/understand-name-free-interaction-for-custom-skills.html>`__

Lambda以外のリソースでのスキルのホスティング
--------------------------------------

SDKはホスティングを可能にする `` ask-sdk-webservice-support``パッケージを提供します
カスタムWebサービスとしてのスキルフレームワーク固有のアダプタも提供します。
統合するために `` flask-ask-sdk``と `` django-ask-sdk``パッケージの下に
それぞれのフレームワークのスキルとWebサービスとして展開します。

これらのパッケージの使用方法に関する詳細はこちらにあります。
`ドキュメントのリンク<https://alexa-skills-kit-python-sdk.readthedocs.io/ja/latest/WEBSERVICE_SUPPORT.html>` __。


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

