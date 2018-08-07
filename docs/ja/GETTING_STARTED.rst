===================
ASK SDKのセットアップ
===================

はじめに
-------

このガイドでは、Alexaスキルを開発する準備としてASK SDK for
Pythonをインストールする方法を説明します。

前提条件
-------

ASK SDK for Pythonには\ **Python 2（2.7以上）**\ または\ **Python
3（3.6以上）**\ が必要です。続行する前に、サポートされているバージョンのPythonがインストールされていることを確認してください。バージョンを表示するには、コマンドプロンプトから以下のコマンドを実行します。

.. code-block:: sh

    $ python --version
    Python 3.6.5

Pythonの最新バージョンは\ `ここ <https://www.python.org/downloads/>`__\ からダウンロードできます。

ASK SDK for Pythonをプロジェクトに追加する
---------------------------------------

ASK SDK for Pythonは、Python Package
Index（PyPI）からコマンドラインツールpipを使用してダウンロードおよびインストールできます。Python
2バージョン2.7.9以降またはPython
3バージョン3.4以降を使用している場合、pipはPythonとともにデフォルトでインストールされています。

多くのPython開発者は仮想環境で作業をおこないます。隔離されたPython環境として使用でき、プロジェクトの依存関係やパッケージのバージョンの管理に便利であるためです。SDKを仮想環境にインストールするのが、最も簡単な開始方法です。\ `SDKを仮想環境にセットアップする <#sdk>`__\ セクションを参照してください。

もうひとつの選択肢は、ASK SDK for
Pythonを特定のフォルダーにインストールすることです。こうすることで、必要な依存関係を確実にインストールでき、完成したスキルに必要なファイルを簡単に見つけてデプロイできます。\ `SDKを特定のフォルダーにセットアップする <#id3>`__\ セクションを参照してください。

オプション1： SDKを仮想環境にセットアップする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下のコマンドを使用して仮想環境を作成し、作成したフォルダーに移動します。

.. code-block:: sh

    $ virtualenv skill

次に、仮想環境をアクティブ化します。MacOSまたはLinuxを使用している場合は、以下のコマンドを使用します。

.. code-block:: sh

    $ source skill/bin/activate

Windowsユーザーの場合は、以下のコマンドを使用します。

.. code-block:: bat

    $ skill\Scripts\activate

コマンドプロンプトのプレフィックスが、仮想環境内部で作業していることを示す（skill）になります。以下のコマンドを使用してASK
SDK for Pythonをインストールします。

.. code-block:: sh

    $ pip install ask-sdk

MacOSおよびLinuxでは、使用するPythonのバージョンによって、SDKがskill/lib/Python3.6/site-packagesフォルダーにインストールされます。Windowsでは、skill\Lib\site-packagesにインストールされます。site-packagesフォルダー内には次のようなディレクトリがあります。

.. code-block:: sh

    ask_sdk
    ask_sdk_core
    ask_sdk_dynamodb
    ask_sdk_model
    boto3
    …

オプション2： SDKを特定のフォルダーにセットアップする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最初に、コマンドプロンプトからAlexaスキル用の新規フォルダーを作成して、そのフォルダーに移動します。

.. code-block:: sh

    $ mkdir skill
    $ cd skill

次に、pipを使用してASK SDK for
Pythonをインストールします。-tというオプションは、特定のフォルダーをインストールのターゲットにします。

.. code-block:: sh

    $ pip install ask-sdk -t ask-sdk

このコマンドはスキルフォルダー内にask-sdkというフォルダーを作成してASK
SDK for
Pythonとその依存関係をインストールします。これで、スキルディレクトリにはフォルダー​ask-sdkが含まれ、その中には次のディレクトリが含まれているはずです。

.. code-block:: sh

    ask_sdk
    ask_sdk_core
    ask_sdk_dynamodb
    ask_sdk_model
    boto3
    …

.. note::

    Mac OS
    Xを使用しており\ `Homebrew <http://brew.sh/>`__\ を使用してPythonをインストールしている場合は、上記のコマンドは機能しません。次の内容のsetup.cfgファイルを\ **ask-sdk**\ ディレクトリに追加することで、この問題を簡単に回避できます。

    .. code-block:: sh

            [install]
            prefix=

    ask-sdkフォルダーに移動して、pip installコマンドを実行します。

    .. code-block:: sh

        $ cd ask-sdk
        $ pip install ask-sdk -t .

    詳細については\ `homebrewドキュメント <https://github.com/Homebrew/brew/blob/master/docs/Homebrew-and-Python.md#setuptools-pip-etc>`__\ で確認してください。​

次のステップ
----------

プロジェクトにSDKを追加したので、スキルの開発を開始できます。次の\ `初めてのスキル開発 <DEVELOPING_YOUR_FIRST_SKILL.html>`__\ セクションに進み、基本のスキル開発の手順をご覧ください。
