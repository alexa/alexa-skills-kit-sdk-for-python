====================================
﻿カスタムスキルをウェブサービスとしてホスティングする
====================================

ウェブサービスを実装してAlexa用のカスタムスキルを開発できます。このウェブサービスは、クラウド内のAlexaサービスからリクエストを受け付けて応答を返します。

Alexaから送信されたリクエストを処理するには、特定の要件を満たす必要があり、また、Alexa Skills Kitインターフェース規格に準拠する必要があります。詳細については、Alexa Skills Kit技術資料の「﻿カスタムスキルをウェブサービスとしてホスティングする<https://developer.amazon.com/ja/docs/custom-skills/host-a-custom-skill-as-a-web-service.html>﻿」__
を参照してください。

.. note::

    現在、これらの機能はベータ版です。ソースコードは、
    GitHubの
    `Ask Python Sdk <https://github.com/alexa/alexa-skills-kit-sdk-for-python>`__
    リポジトリで確認できます。正式版のリリース時に、インターフェースが変更される可能性が
    あります。

ASD SDKウェブサービスサポート
---------------------------

Alexa Skills Kit SDK（ASK SDK）for Pythonでは、リクエストとタイムスタンプの検証用のボイラープレートコードが「ask-sdk-webservice-support <https://pypi.org/project/ask-sdk-webservice-support/>」__パッケージで提供されます。これは`Skill Builder <SKILL_BUILDERS.html>`__ オブジェクトと統合されます。このパッケージでは検証コンポーネントと、スキルを呼び出すためのベースハンドラーのみが提供され、ウェブアプリケーション開発の基本フレームワークからは独立しています。

インストール
~~~~~~~~~~~~

「pip」を使用して``ask-sdk-webservice-support``パッケージをインストールします。

.. important::

    このパッケージは、リクエスト検証用の`cryptography <https://cryptography.io/en/latest/>`__に依存しています。また、「cryptography」パッケージは、オペレーティングシステムに応じて追加条件がある場合があります。詳細については、`cryptography」ドキュメントの「インストールガイド<https://cryptography.io/en/latest/installation/>`__ を参照してください。

ウェブサービスジェネリックハンドラー
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``WebserviceSkillHandler``クラスでは、``SkillBuilder``オブジェクトからスキルインスタンスを登録し、``verify_request_and_dispatch``メソッドを提供します。このメソッドは、スキルハンドラーを呼び出す前に入力リクエストを検証します。

``WebserviceSkillHandler``インスタンスのboolean型パラメーター``verify_signature``および``verify_timestamp``を設定し、テスト目的として、リクエストまたはタイムスタンプの検証を有効または無効にできます。また、スキルを呼び出す前に入力リクエストに適用する必要がある、追加のカスタムベリファイア（verifier）も提供されます。

``verify_request_and_dispatch``メソッドにより、ウェブサービスから``http_headers``と``http_body``が取り出され、スキルの呼び出しに成功すると、文字列形式で``response``が返されます。入力と出力をウェブサービス固有のリクエスト／応答の構造に変換する必要があります。

使用形態
~~~~~

.. code-block:: python

    from ask_sdk_core.skill_builder import SkillBuilder
    from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler

    skill_builder = SkillBuilder()

    # リクエストハンドラー、例外ハンドラーなどを実装します。
    # ハンドラーをスキルビルダーインスタンスに登録します。

    webservice_handler = WebserviceSkillHandler(
        skill=skill_builder.create())

    # HTTPリクエストヘッダーと本文をそれぞれネイティブ形式の
    # dictとstrに変換し、dispatchメソッドを呼び出します。
    response = webservice_handler.verify_request_and_dispatch(
        headers, body)

    # 応答strをウェブサービスの形式に変換して返します。


フレームワーク固有のアダプター
-----------------

Pythonには、FlaskとDjangoという2つのウェブサービスフレームワークがあり、ウェブサービスを開発するときによく活用されています。
ASK SDKでは、フレームワーク別に``ask-sdk-webservice-support``パッケージの拡張機能が提供され、FlaskとDjangoの両方に対応しています。
これにより、リクエスト／応答の変換処理が内部で行われます。さらに、既に開発しているSDKスキルを簡単に統合して、ウェブサービスで動作させることができます。

flask-ask-sdk拡張パッケージ
~~~~~~~~~~~~~~~~~~~~~~

``flask-ask-sdk``パッケージは、Flaskの拡張機能を提供します。これにより、カスタムスキルと一緒に``Flask``アプリケーションを登録できます。helperメソッドも提供され、スキルの呼び出しを、URLエンドポイントとしてFlaskアプリケーションに登録できます。

``flask-ask-sdk``パッケージは、`Flask拡張機能の構造<http://flask.pocoo.org/docs/1.0/extensiondev/#flask-extension-development>`__ に従っています。
「SkillAdapter」クラスのコンストラクターで、以下を取り出します。

-「スキル」インスタンス
-「skill id」（拡張ディレクトリにスキルインスタンスを登録する）
-「Flask」アプリケーション（オプション。アプリケーションに拡張機能を登録する）

また、``init_app``メソッドも提供され、後でFlaskアプリインスタンスに渡され、拡張機能のインスタンスを作成し構成します。

リクエストとタイムスタンプの検証はデフォルトで有効になっています。アプリコンフィギュレーション``VERIFY_SIGNATURE_APP_CONFIG``と``VERIFY_TIMESTAMP_APP_CONFIG``を使用して、それぞれのboolean値を設定し、検証の有効／無効を設定できます。

SkillAdapterの``dispatch_request``メソッドを使用して、スキルをエンドポイントURLルールとして登録できます。リクエスト／応答の変換処理、リクエストとタイムスタンプの検証、スキルの呼び出しを処理します。

インストール
``````

「pip」を使用して``flask-ask-sdk``パッケージをインストールできます。

.. important::

    また、`cryptography <https://cryptography.io/en/latest/>`__
    パッケージが、リクエスト検証の依存関係として含まれています。また、「cryptography」パッケージは、オペレーティングシステムに応じて追加条件がある場合があります。詳細については、「cryptography」ドキュメントの「インストールガイド<https://cryptography.io/en/latest/installation/>」__を参照してください。

使用形態
````````

.. code-block:: python

    from flask import Flask
    from ask_sdk_core.skill_builder import SkillBuilder
    from flask_ask_sdk.skill_adapter import SkillAdapter

    app = Flask(__name__)
    skill_builder = SkillBuilder()
    # インテントハンドラーをskill_builderオブジェクトに登録します。

    skill_adapter = SkillAdapter(
        skill=skill_builder.create(), skill_id=<SKILL_ID>, app=app)

    @app.route("/"):
    def invoke_skill:
        return skill_adapter.dispatch_request()

.. note::

    「ASK_SDK_SKILL_ADAPTER」キーを使用して、拡張機能のインスタンスが
    アプリケーション拡張機能マッピングに追加されます。同じアプリケーション内の
    異なるルートに複数のスキルが構成されるので、
    複数の拡張機能インスタンスを介して、それぞれの拡張機能が
    スキルIDマッピングとして、アプリ拡張機能の「ASK_SDK_SKILL_ADAPTER」ディクショナリに
    追加されます。

django-ask-sdk拡張パッケージ
~~~~~~~~~~~~~~~~~~~~~~~

``django-ask-sdk``拡張パッケージにより、Djangoの拡張機能が提供され、エンドポイントとして、カスタムスキルをDjangoアプリケーションに登録できます。

拡張機能では``SkillAdapter``ビュークラスが提供されます。カスタムスキルインスタンスでビュークラスをインスタンス化し、ASK SDK Skill Builderオブジェクトでビルドし、Djangoアプリの``urls.py``ファイルに登録します。これにより、対応するエンドポイントでスキルが呼び出されます。

リクエストとタイムスタンプの検証はデフォルトで有効になっています。コンストラクター引数``verify_request``と``verify_timestamp``を使用して、それぞれのboolean値を設定することで、各検証を有効または無効にできます。

インストール
``````

「pip」を使用して``django-ask-sdk``拡張機能をインストールできます。

.. important::

    また、`cryptography <https://cryptography.io/en/latest/>`__ パッケージが、リクエスト検証の依存関係として含まれています。また、「cryptography」パッケージは、オペレーティングシステムに応じて追加条件が
    ある場合があります。詳細については、「cryptography」ドキュメントの`インストールガイド<https://cryptography.io/en/latest/installation/>`__ を参照してください。

.. note::

    Django 2.0はPython 3のみをサポートしているため、これに依存する
    ``django-ask-sdk``パッケージは、Python3.0以降と互換性があります。

使用形態
````````

``SkillBuilder``インスタンスを使用してスキルを開発する場合は、
``example.urls.py``で以下を使用すると、
``example``というDjangoアプリで、エンドポイントとしてスキルを登録できます。

.. code-block:: python

    import skill
    from django_ask_sdk.skill_response import SkillAdapter

    view = SkillAdapter.as_view(skill=skill.sb.create())

    urlpatterns = [
        path("/myskill", view, name='index')
    ]
