import os
import pytest

from operator import attrgetter

from lemon import api
from lemon.api import Api

API_KEY = os.getenv('API_KEY', None)


@pytest.fixture
def uut() -> Api:
    return api.create(api_token=API_KEY)


@pytest.mark.parametrize('type_', ["stock", "bond", "fund", "etf"])
def test_instruments_by_type(uut: Api, type_):
    result = uut.market_data.instruments.get(type=[type_])
    assert set(map(attrgetter('type'), result.results)) == {type_}


def test_instruments_by_search(uut: Api):
    result = uut.market_data.instruments.get(search='tesla*')
    assert len(result.results) == 3


def test_instruments_by_isin(uut: Api):
    response = uut.market_data.instruments.get(isin=['US88160R1014'])

    assert len(response.results) == 1
    assert response.results[-1].title == 'TESLA INC.'


@pytest.mark.parametrize('currency', ['EUR', 'PLN'])
def test_instruments_by_currency(uut: Api, currency):
    response = uut.market_data.instruments.get(currency=currency)

    given = set()
    for instrument in response.results:
        given.update(info.currency for info in instrument.venues)
    assert given == {currency}


@pytest.mark.parametrize('tradable', [True, False])
def test_instruments_by_tradable(uut: Api, tradable: bool):
    response = uut.market_data.instruments.get(tradable=tradable)

    given = set()
    for i in response.results:
        given.update(info.tradable for info in i.venues)
    assert given == {tradable}


def test_instruments_limit(uut: Api):
    response = uut.market_data.instruments.get(limit=10)
    assert len(response.results) == 10
