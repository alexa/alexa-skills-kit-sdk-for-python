Alexaサービスクライアント
======================

SDKには、スキルのロジックからAlexa APIを呼び出すために使用できるサービスクライアントが含まれています。

サービスクライアントは、リクエストハンドラー、例外ハンドラー、リクエストと応答のインターセプターで使用できます。\ `ハンドラー入力 <REQUEST_PROCESSING.html#id2>`__\ に含まれる ``service_client_factory`` により、サポートされているすべてのAlexaサービスのクライアントインスタンスを取得することができます。``service_client_factory`` は、``ApiClient`` を使用して\ `スキルのインスタンスを設定 <SKILL_BUILDERS.html#skill-builders>`__\ する場合にのみ使用できます。

以下は、リクエストハンドラーの ``handle`` 関数の例です。デバイスアドレスサービスクライアントのインスタンスが作成されます。サービスクライアントインスタンスは、適切なfactory関数を呼び出すのと同じくらい簡単に作成できます。

.. code:: python

    def handle(handler_input):
        device_id = handler_input.request_envelope.context.system.device.device_id
        device_addr_service_client = handler_input.service_client_factory.get_device_address_service()
        addr = device_addr_service_client.get_full_address(device_id)
        # Other handler logic goes here
        ....
