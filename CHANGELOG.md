# 1.0.0

- Support those requests in the library:

  - [Market Data API](https://docs.lemon.markets/market-data/overview)

    - [GET /instruments/](https://docs.lemon.markets/market-data/instruments-tradingvenues#get-instruments)
    - [GET /ohlc/{x1}/](https://docs.lemon.markets/market-data/historical-data#get-ohlcx1)
    - [GET /quotes/latest/](https://docs.lemon.markets/market-data/historical-data#get-quoteslatest)
    - [GET /trades/latest/](https://docs.lemon.markets/market-data/historical-data#get-tradeslatest)
    - [GET /venues/](https://docs.lemon.markets/market-data/instruments-tradingvenues#get-venues)

  - [Trading API](https://docs.lemon.markets/trading/overview)

    - [GET /account/](https://docs.lemon.markets/trading/account#get-account)
    - [PUT /account/](https://docs.lemon.markets/trading/account#put-account)
    - [GET /account/withdrawals/](https://docs.lemon.markets/trading/account#get-accountwithdrawals)
    - [POST /account/withdrawals/](https://docs.lemon.markets/trading/account#post-accountwithdrawals)
    - [GET /account/bankstatements/](https://docs.lemon.markets/trading/account#get-accountbankstatements)
    - [GET /account/documents/](https://docs.lemon.markets/trading/account#get-accountdocuments)
    - [PUT /account/documents/{document_id}/](https://docs.lemon.markets/trading/account#get-accountdocumentsdocument_id)
    - [GET /orders/](https://docs.lemon.markets/trading/orders#get-orders)
    - [POST /orders/](https://docs.lemon.markets/trading/orders#post-orders)
    - [POST /orders/{order_id}/activate/](https://docs.lemon.markets/trading/orders#post-ordersorder_idactivate)
    - [GET /orders/{order_id}/](https://docs.lemon.markets/trading/orders#get-ordersorder_id)
    - [DELETE /orders/{order_id}/](https://docs.lemon.markets/trading/orders#delete-ordersorder_id)
    - [GET /positions/](https://docs.lemon.markets/trading/positions#get-positions)
    - [GET /positions/statements/](https://docs.lemon.markets/trading/positions#get-positionsstatements)
    - [GET /positions/performance/](https://docs.lemon.markets/trading/positions#get-positionsperformance)
    - GET /user/

- Implement error handling
- Allow changing default timeout
- Allow changing default retry_count
- Allow changing default retry_backoff_factor
- Allow changing default pool_connections
- Allow changing default pool_maxsize
