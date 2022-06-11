# lemon.markets Python Library

[![Licence](https://img.shields.io/github/license/lemon-markets/sdk-python)](./LICENSE)
[![GiTests](https://img.shields.io/github/workflow/status/lemon-markets/sdk-python/tests/main?label=tests)](https://github.com/lemon-markets/sdk-python/actions)
[![Python versions](https://img.shields.io/pypi/pyversions/lemon.svg)](https://pypi.python.org/pypi/lemon/)
[![pypi](https://img.shields.io/pypi/v/lemon)](https://pypi.python.org/pypi/lemon/)

The lemon.markets Python Library provides convenient access to the [lemon.markets](https://docs.lemon.markets/) API from applications written in the Python language.

The library fully supports:

- [Market Data API](https://docs.lemon.markets/market-data/overview)
- [Trading API](https://docs.lemon.markets/trading/overview)

# Installation

You can install the library by using [pip](http://pypi.python.org/pypi/pip):

    pip install lemon

# Example usage

Before making API calls, we need to provide API token. Information on how to generate an API token can be found [here](https://docs.lemon.markets/authentication).

**Market API**

```python
import lemon
client = lemon.create(api_token='...')

# list instruments
instruments = client.market_data.instruments.get()

# print the first instrument's name
print(instruments.results[0].name)
```

**Trading API**

```python
import lemon
client = lemon.create(api_token='...')

# delete order
client.trading.orders.delete('125488fd')
```

# Error handling

TBD

# Direct API calls

Both `client.trading` and `client.market_data` allows calling underlining API directly.

```python
import lemon
client = lemon.create(api_token='...')

# edit account data
client.trading.put(url='account', json={"address_street": address_street})
```
