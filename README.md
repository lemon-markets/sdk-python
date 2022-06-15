# lemon.markets Python Library

[![License](https://img.shields.io/github/license/lemon-markets/sdk-python)](./LICENSE)
[![Tests](https://img.shields.io/github/workflow/status/lemon-markets/sdk-python/tests/main?label=tests)](https://github.com/lemon-markets/sdk-python/actions)
[![Python versions](https://img.shields.io/pypi/pyversions/lemon.svg)](https://pypi.python.org/pypi/lemon/)
[![PyPI](https://img.shields.io/pypi/v/lemon)](https://pypi.python.org/pypi/lemon/)

The lemon.markets Python Library provides convenient access to the [lemon.markets](https://docs.lemon.markets/) API from applications written in the Python language.
The library contains synchronous client that can be shared across threads.

The library fully supports:

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

# Installation

You can install the library by using [pip](http://pypi.python.org/pypi/pip):

    pip install lemon

# Example usage

Before making API calls, we need to provide API token.
Information on how to generate an API token can be found [here](https://docs.lemon.markets/authentication).

**Market API**

```python
import requests

from lemon import api, errors

client = api.create(api_token="...")

try:
    # list instruments
    instruments = client.market_data.instruments.get(isin="US88160R1014")
    print(instruments.results[0].name)

    # list ohlc
    ohlc = client.market_data.ohlc.get(
        isin=["US88160R1014"], period="m1", from_="latest"
    )
    print(ohlc.results[0].pbv)

    # list quotes
    quotes = client.market_data.quotes.get_latest(isin=["US88160R1014"])
    print(quotes.results[0].b_v)
except errors.BusinessLogicError as exc:
    print(exc.error_message)
except errors.InvalidRequestError as exc:
    print(exc.error_message)
except errors.AuthenticationError as exc:
    print(exc.error_message)
except errors.InternalServerError as exc:
    print(exc.error_message)
except errors.APIError as exc:
    print(exc.data)
except requests.RequestException:
    print("timeout or maximum number of retries exceeded")
```

**Trading API**

You can pass `money` or `paper` to the `env` parameter in order to select appropriate trading environment.
More information about lemon.market environments can be found [here](https://docs.lemon.markets/trading/overview#general-things).

```python
import requests

from lemon import api, errors

client = api.create(api_token="...", env="money")

try:
    # create order
    created_order = client.trading.orders.create(
        isin="US88160R1014", side="sell", quantity=50
    )
except errors.BusinessLogicError as exc:
    print(exc.error_message)
except errors.InvalidRequestError as exc:
    print(exc.error_message)
except errors.AuthenticationError as exc:
    print(exc.error_message)
except errors.InternalServerError as exc:
    print(exc.error_message)
except errors.APIError as exc:
    print(exc.data)
except requests.RequestException:
    print("timeout or maximum number of retries exceeded")
```

# Configuration

`lemon.api.create` allows to configure wide set of parameters:

- `api_token` - a token to be used in the authentication process.
- `env` - selects trading environment to be used.
- `timeout` - how long to wait for the server to send data before giving up.
- `retry_count` - the maximum number of retries each connection should attempt.
- `retry_backoff_factor` - a backoff factor to apply between attempts after the second try.
- `pool_connections` - the number of urllib3 connection pools to cache.
- `pool_maxsize` - the maximum number of connections to save in the pool.

# Error handling

Unsuccessful requests throws exceptions. The library may throw those exceptions:

- [`lemon.errors.APIError`](./lemon/errors.py) - is thrown when an unknown error is received.
- [`lemon.errors.InvalidRequestError`](./lemon/errors.py) - thrown when an invalid request error is received from the API.
- [`lemon.errors.AuthenticationError`](./lemon/errors.py) - thrown when an authorization error is received from the API.
- [`lemon.errors.InternalServerError`](./lemon/errors.py) - is thrown when an internal server error is received from the API.
- [`lemon.errors.BusinessLogicError`](./lemon/errors.py) - thrown on receiving any other error from the API.
- [`requests.RequestExceptions`](https://requests.readthedocs.io/en/latest/api/#requests.RequestException) - thrown by `requests` on network error, timeout, max retry count reached etc.
- [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) - thrown when the library encounters invalid input.

`lemon.errors.InvalidRequestError`, `lemon.errors.AuthenticationError`, `lemon.errors.InternalServerError` and `lemon.errors.BusinessLogicError`
contains those properties:

- `error_code` - contains unique error type identifier.
- `error_message` - contains human-readable description of the error.

List of all error codes can be found [here](https://docs.lemon.markets/error-handling).

More information about exceptions that can be thrown by `requests` can be found [here](https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions).

# Direct API calls

Both `client.trading` and `client.market_data` allows calling underlining API directly.
`get/post/put/delete` methods will handle authorization and error handling. The library will join URLs in the same way as [urllib.parse.urljoin](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin).

```python
import requests

from lemon import api, errors

client = api.create(api_token="...")

try:
    # edit account data
    resp = client.trading.put(url="account", json={"address_street": address_street})
    # handle ok response
    ...
except errors.BusinessLogicError as exc:
    print(exc.error_message)
except errors.InvalidRequestError as exc:
    print(exc.error_message)
except errors.AuthenticationError as exc:
    print(exc.error_message)
except errors.InternalServerError as exc:
    print(exc.error_message)
except errors.APIError as exc:
    print(exc.data)
except requests.RequestException:
    print("timeout or maximum number of retries exceeded")
```

# License

The library is published under [MIT License](./LICENSE)
