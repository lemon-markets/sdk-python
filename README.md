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

## Usage

### SDK client

To create and configure SDK client you will need have separate API tokens for `Market Data API` and `Trading API`
and point out which environment you want to use for trading - paper or money (default is paper).
The description of creating and using API tokens is described [here](https://docs.lemon.markets/authentication).
Snippet below shows how to properly create SDK client object:

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

SDK client consists of two parts:

- `matket_data` - contains references to Market Data API endpoints
- `trading` - contains references to Trading API endpoints. SDK communicates with either paper or money environment,
  depending on the client configuration.


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
response = client.market_data.instruments.get(isin=["US88160R1014", "US0231351067"])
response = client.market_data.instruments.get(search='t*a', tradable=True)
response = client.market_data.instruments.get(type=['stock', 'etf'], currency=['EUR'], limit=10, sorting='asc')

# get latest ohlc
response = client.market_data.ohlc.get(isin=['US88160R1014'], from_='latest', epoch=True, decimals=True)

# get ohlc
response = client.market_data.ohlc.get(isin=['US88160R1014'], from_=datetime(2021, 1, 2))

# get latest quotes
response = client.market_data.quotes.get_latest(isin=['US88160R1014', 'US0231351067'], epoch=True, sorting='asc')

# get trades
response = client.market_data.trades.get_latest(isin=['US88160R1014', 'US0231351067'], decimals=True)
```

### Trading API usage

```python
from lemon import api

client = api.create(...)

# create buy order
response = client.trading.orders.create(isin='US88160R1014', side='buy', quantity=1)
order_id = response.results.id

# activate buy order
response = client.trading.orders.activate(order_id=order_id)

# get order
response = client.trading.orders.get(order_id=order_id)

# get orders
response = client.trading.orders.get()

# create sell order
response = client.trading.orders.create(isin='US88160R1014', side='sell', quantity=1)
order_id = response.results.id

# activate sell order
response = client.trading.orders.activate(order_id=order_id)

# get account
response = client.trading.account.get()

# update account
response = client.trading.account.update(address_street='Ritterstrasse', address_street='Berlin')

# withdraw money from account
response = client.trading.account.withdraw(amount=100000, pin="1234")

# get bank statements
response = client.trading.account.get_bank_statements(type='eod_balance',
from="beginning")

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
### Error handling
```

### Direct API calls
Both `client.trading` and `client.market_data` allows calling underlining API directly.
`GET/POST/PUT/DELETE` methods will handle authorization and error handling. The library will join URLs in the same way
as [urllib.parse.urljoin](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin).

```python
from lemon import api

client = api.create(...)
resp = client.trading.put(url="account", json={"address_street": 'New street name'})
```

### Error handling
The hierarchical error structure available in the SDK is presented below

BaseLemonError - The base class for all errors thrown within the SDK
 LemonError - the base class of errors that are returned at the API level. It contains information directly from the API, such as status, error_code, error_message, time
     InvalidQueryError - HTTP request validation error
     AuthenticationError - authorization error
     InternalServerError - internal API error
     BusinessLogicError - a business logic error that prevents the request from being fulfilled due to specific conditions that have occurred
 APIError - API error, thrown in case

Please note that errors coming directly from the `request` module are passed as is.
```python
from lemon import api

client = api.create(...)

try:
    response = client.trading.orders.create(isin='...', side='buy', quantity=1)
except errors.InvalidRequestError:
    ...
except errors.AuthenticationError:
    ...
except InternalServerError:
    ...
except BusinessLogicError:
    ...
except LemonError: # catches InvalidRequestError/AuthenticationError/InternalServerError/BusinessLogicError
    ...
except APIError:
    ...
except BaseLemonError: # catches all errors defined above
    ...
except: # other errors
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


