# lemon.markets Python SDK

[![License](https://img.shields.io/github/license/lemon-markets/sdk-python)](./LICENSE)
[![Tests](https://img.shields.io/github/workflow/status/lemon-markets/sdk-python/tests/main?label=tests)](https://github.com/lemon-markets/sdk-python/actions)
[![Python versions](https://img.shields.io/pypi/pyversions/lemon.svg)](https://pypi.python.org/pypi/lemon/)
[![PyPI](https://img.shields.io/pypi/v/lemon)](https://pypi.python.org/pypi/lemon/)

[lemon.markets](https://lemon.markets) Python SDK facilitates communication with the
[lemon.markets](https://lemon.markets) API for Python programs. The library implements all calls to the endpoints
defined in the Market Data API and Trading API. We currently do not support asynchronous calls.

## Documentation

See the [API docs](https://docs.lemon.markets/).

## Installation

You can install library using [pip](http://pypi.python.org/pypi/pip):

```bash
pip install lemon
````

Requirements:

- Python 3.7+
- `requests`
- `pytz`
- `typing-extensions`

## Usage

### SDK client

To create and configure our SDK client you will need to have separate API tokens for `Market Data API` and `Trading API`. You also need to choose which environment you want to use for trading: `paper` or `money`, defaults to `paper`.
For how to obtain and use our api token, see [here](https://docs.lemon.markets/authentication).
The snippet below shows how to properly create a SDK client:
```python
from lemon import api

client = api.create(
    market_data_api_token='your-market-data-api-token',
    trading_api_token='your-trading-api-token',
    env='paper'  # or env='money'
)
```

`lemon.api.create` method allows also to configure:

- `timeout` - default timeout for requests
- `retry_count` - default number of retries for requests
- `retry_backoff_factor` - default retry backoff factor for retries

The SDK client consists of two parts:

- `market_data` - let's you access the Market Data API endpoints
- `trading` - let's you access the Trading API endpoints. Choose the desired target environment (paper or money) in the client configuration. 

### Market Data API usage

```python
from lemon import api
from datetime import datetime

client = api.create(
    market_data_api_token='your-market-data-api-token',
    trading_api_token='your-trading-api-token',
)

# get venues
response = client.market_data.venues.get()
print(response.results)

# get instruments
response = client.market_data.instruments.get(
    isin=["US88160R1014", "US0231351067"]
)
response = client.market_data.instruments.get(
    search='t*a',
    tradable=True,
)
response = client.market_data.instruments.get(
    type=['stock', 'etf'],
    currency=['EUR'],
    limit=10,
    sorting='asc'
)

# get latest ohlc
response = client.market_data.ohlc.get(
    isin=['US88160R1014'],
    from_='latest',
    epoch=True,
    decimals=True
)

# get ohlc
response = client.market_data.ohlc.get(
    isin=['US88160R1014'],
    from_=datetime(2021, 1, 2)
)

# get latest quotes
response = client.market_data.quotes.get_latest(
    isin=['US88160R1014', 'US0231351067'],
    epoch=True,
    sorting='asc'
)

# get trades
response = client.market_data.trades.get_latest(
    isin=['US88160R1014', 'US0231351067'],
    decimals=True
)
```

### Trading API usage

```python
from lemon import api

client = api.create(...)

# create buy order
response = client.trading.orders.create(
    isin='US88160R1014',
    side='buy',
    quantity=1
)
order_id = response.results.id

# activate buy order
response = client.trading.orders.activate(order_id=order_id)

# get buy order status
response = client.trading.orders.get_order(order_id=order_id)

# get orders
response = client.trading.orders.get()

# cancel order
response = client.trading.orders.create(isin='US88160R1014', side='buy', quantity=1)
response = client.trading.orders.cancel(order_id=response.results.id)

# update account
response = client.trading.account.update(
    address_street='Ritterstrasse',
    address_city="Berlin"
)

# withdraw money from account
response = client.trading.account.withdraw(
    amount=100000,
    pin="1234"
)

# get bank statements
response = client.trading.account.get_bank_statements(
    type='eod_balance',
    from_="beginning"
)

# get documents
response = client.trading.account.get_documents()

# get document
response = client.trading.account.get_document(document_id='doc_xyz')

# get user
response = client.trading.user.get()

# get positions
response = client.trading.positions.get(isin='US88160R1014')

# get statements
response = client.trading.positions.get_statements()

# get performance
response = client.trading.positions.get_performance()
```

### Direct API calls

It is possible to call Market Data API/Trading API endpoints directly by providing path to the endpoint 
and optionally - query parameters and payload to be sent.  SDK currently supports `GET|POST|PUT|DELETE` methods.

```python
from lemon import api

client = api.create(...)

response = client.trading.put(url="account", json={"address_street": 'New street name'})
response = client.market_data.get(url="instruments", params={"search": "t*sla"})
```

### Error handling

Error structure available in the SDK is presented below

* `BaseLemonError` - base class for all errors thrown within the SDK
    * `LemonError` - base class of errors returned by API. It contains information directly from it, such as `status`, `error_code`, `error_message`, ...
        * `InvalidQueryError` - HTTP request validation error
        * `AuthenticationError` - authentication error
        * `InternalServerError` - internal API error
        * `BusinessLogicError` - a business logic error caused by specific conditions of the system preventing from fulfilling the request
    * `APIError` - error thrown in case when it's impossible to decode the API response

Please note that errors raised from `requests` module are passed as they are.

```python
from lemon import api, errors

client = api.create(...)

try:
    response = client.trading.orders.create(isin='...', side='buy', quantity=1)
except errors.InvalidQueryError:
    ...
except errors.AuthenticationError:
    ...
except errors.InternalServerError:
    ...
except errors.BusinessLogicError as err:
    if err.error_code == 'some_specific_error':
        print(err.error_message)
        ... # do something
    ...
except errors.LemonError:  # InvalidRequestError/AuthenticationError/InternalServerError/BusinessLogicError
    ...
except errors.APIError:
    ...
except errors.BaseLemonError:  # catches all errors defined above
    ...
except:  # other errors, including errors from `requests` module
    ...
```

### Model serialization

Every response(or response nested structure) can be serialized to python dictionary or JSON:

```python
from lemon import api

client = api.create(
    market_data_api_token='your-market-data-api-token',
    trading_api_token='your-trading-api-token',
)
response = client.market_data.instruments.get()

print(response.dict())
print(response.json())
print(response.results[0].dict())
print(response.results[0].json())
```


