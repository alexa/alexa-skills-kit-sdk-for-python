===================
スキルのアトリビュート
===================

このガイドでは、スキル開発に使用できるアトリビュートのさまざまなスコープと、スコープをスキルで使用する方法について説明します。

アトリビュート
============

SDKを使うと、さまざまなスコープでアトリビュートの保存と取得ができます。たとえば、アトリビュートを使用して後続のリクエストで取得するデータを保存できます。また、ハンドラーの ``can_handle`` ロジックでアトリビュートを使用して、リクエストのルーティングに条件を追加することもできます。

アトリビュートは、キーと値で構成されます。キーは ``str`` 型限定、値は無制限の ``object`` 型です。セッションアトリビュートと永続アトリビュートの場合、値は保存して後で取得できるよう、シリアライズできるデータ型である必要があります。この制限はリクエストレベルのアトリビュートには適用されません。なぜならリクエストレベルのアトリビュートは、リクエスト処理のライフサイクルが終了すると、永続的に存在しないからです。

アトリビュートのスコープ
=====================

リクエストアトリビュート
~~~~~~~~~~~~~~~~~~~~~

リクエストアトリビュートは、1回のリクエスト処理ライフサイクルの間のみ存続します。リクエストを受信した時点では、リクエストアトリビュートは空です。また応答が生成されると破棄されます。

リクエストアトリビュートは、リクエストと応答のインターセプターと合わせて使うと便利です。たとえば、リクエストインターセプターを使って追加のデータとヘルパーメソッドをリクエストアトリビュートに挿入して、リクエストハンドラーが取得できるようにできます。

セッションアトリビュート
~~~~~~~~~~~~~~~~~~~~~

セッションアトリビュートは、現在のスキルセッションが継続している間存続します。セッションアトリビュートは、すべてのセッション内リクエストで使用できます。リクエスト処理のライフサイクル中に設定されたすべてのアトリビュートはAlexaサービスに返され、同じセッションの次のリクエストで提供されます。

セッションアトリビュートで、外部ストレージソリューションを使用する必要はありません。セッションアトリビュートはセッション外のリクエストの処理では使用できません。スキルセッションがクローズされると破棄されます。

永続アトリビュート
~~~~~~~~~~~~~~~~

永続アトリビュートは、現在のセッションのライフサイクルが終了しても存続します。主要なスコープ（ユーザーID、デバイスID）、TTL、ストレージレイヤーを含む、これらのアトリビュートがどのように保存されるかはスキルのコンフィギュレーションによって異なります。

永続アトリビュートは、``PersistenceAdapter`` を使用して\ `スキルのインスタンスを設定 <SKILL_BUILDERS.html#skill-builders>`__\ する場合にのみ使用できます。``PersistenceAdapter`` が設定されていない場合に、``AttributesManager`` を呼び出して永続アトリビュートの取得と保存を行おうとするとエラーが発生します。

PersistenceAdapter
==================

``AbstractPersistenceAdapter`` は、永続レイヤー（データベースやローカルファイルシステムなど）でアトリビュートを保存したり取得したりする場合に ``AttributesManager`` が使用します。``ask-sdk-dynamodb-persistence-adapter`` パッケージは、\ `AWS DynamoDB <https://aws.amazon.com/dynamodb/>`__\ を使用してAbstractPersistenceAdapterを実装します。

``AbstractPersistenceAdapter`` の実装はすべて、以下のインターフェースに従う必要があります。

インターフェース
~~~~~~~~~~~~~~

.. code:: python

    class AbstractPersistenceAdapter(object):
        def get_attributes(self, request_envelope):
            # type: (RequestEnvelope) -> Dict[str, Any]
            pass

        def save_attributes(self, request_envelope, attributes):
            # type: (RequestEnvelope, Dict[str, Any]) -> None
            pass

AttributesManager
=================

AttributesManagerには、ハンドラーで取得や更新を行えるアトリビュートがあります。AttributesManagerは、`Handler Input <REQUEST_PROCESSING.html#id2>`__ オブジェクトからハンドラーで使用できます。``AttributesManager`` は、スキルで必要なアトリビュートと直接やり取りできるように、アトリビュートの取得と保存を行います。

インターフェース
~~~~~~~~~~~~~~

.. code:: python

    class AttributesManager(object):
        def __init__(self, request_envelope, persistence_adapter=None):
            # type: (RequestEnvelope, AbstractPersistenceAdapter) -> None
            ....

        @property
        def request_attributes(self):
            # type: () -> Dict[str, Any]
            # Request Attributes getter
            ....

        @request_attributes.setter
        def request_attributes(self, attributes):
            # type: (Dict[str, Any]) -> None
            # Request Attributes setter
            ....

        @property
        def session_attributes(self):
            # type: () -> Dict[str, Any]
            # Session Attributes getter
            ....

        @session_attributes.setter
        def session_attributes(self, attributes):
            # type: (Dict[str, Any]) -> None
            # Session Attributes setter
            ....

        @property
        def persistent_attributes(self):
            # type: () -> Dict[str, Any]
            # Persistence Attributes getter
            # Uses the Persistence adapter to get the attributes
            ....

        @persistent_attributes.setter
        def persistent_attributes(self, attributes):
            # type: (Dict[str, Any]) -> None
            # Persistent Attributes setter
            ....

        def save_persistent_attributes(self):
            # type: () -> None
            # Persistence Attributes save
            # Save the Persistence adapter to save the attributes
            ....


以下は、永続アトリビュートの取得と保存を行う方法のサンプルです。

.. code:: python

    class PersistenceAttributesHandler(AbstractRequestHandler):
        def can_handle(handler_input):
            persistence_attr = handler_input.attributes_manager.persistent_attributes
            return persistence_attr['foo'] == 'bar'

        def handle(handler_input):
            persistence_attr = handler_input.attributes_manager.persistent_attributes
            persistence_attr['foo'] = 'baz'
            handler_input.attributes_manager.save_persistent_attributes()
            return handler_input.response_builder.response
