=======
サンプルスキル
=======

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
