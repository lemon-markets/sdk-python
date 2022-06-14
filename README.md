# lemon.markets Python Library

[![Licence](https://img.shields.io/github/license/lemon-markets/sdk-python)](./LICENSE)
[![Tests](https://img.shields.io/github/workflow/status/lemon-markets/sdk-python/tests/main?label=tests)](https://github.com/lemon-markets/sdk-python/actions)
[![Python versions](https://img.shields.io/pypi/pyversions/lemon.svg)](https://pypi.python.org/pypi/lemon/)
[![PyPI](https://img.shields.io/pypi/v/lemon)](https://pypi.python.org/pypi/lemon/)

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
import requests

from lemon import api, errors

client = api.create(api_token="...")

try:
    # list instruments
    instruments = client.market_data.instruments.get()
    print(instruments.results[0].name)
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

# Error handling

The library may throw those exceptions:

- [`lemon.errors.BusinessLogicError`](./lemon/errors.py) - thrown on receiving most errors from the API.
- [`lemon.errors.InvalidRequestError`](./lemon/errors.py) - thrown when an invalid request error is received from the API.
- [`lemon.errors.AuthenticationError`](./lemon/errors.py) - thrown when an authorization error is received from the API.
- [`lemon.errors.InternalServerError`](./lemon/errors.py) - is thrown when an internal server error is received from the API.
- [`lemon.errors.APIError`](./lemon/errors.py) - is thrown when an unknown error is received.
- [`requests.RequestExceptions`](https://requests.readthedocs.io/en/latest/api/#requests.RequestException) - thrown by `requests` on network error, timeout, max retry count reached etc.

More information about exceptions that can be thrown by `requests` can be found [here](https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions).

List of all error codes can be found [here](https://docs.lemon.markets/error-handling).

# Direct API calls

Both `client.trading` and `client.market_data` allows calling underlining API directly.
`get/post/put/delete` methods will handle authorization and error handling.

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
