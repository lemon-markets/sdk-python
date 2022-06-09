import os
from dataclasses import asdict
from pprint import pprint

import pytest

from lemon import api
from lemon.api import Api

API_KEY = os.getenv('API_KEY', None)


@pytest.fixture
def uut() -> Api:
    return api.create(api_token=API_KEY)


def test_instruments(uut: Api):
    result = uut.market_data.instruments.get(search='a*bet', type=['etf', 'stock'])

    pprint(asdict(result))

    for instrument in result.results:
        print(instrument.title)


def test_order(uut: Api):
    result = uut.market_data.instruments.get(
        search='TESLA'
    )

    result = uut.trading.orders.create(
        isin=result.results[-1].isin,
        side='buy',
        quantity=5,
        expires_at=5,
    )
    result = uut.trading.orders.activate(order_id=result.results.id)
    print(result)
