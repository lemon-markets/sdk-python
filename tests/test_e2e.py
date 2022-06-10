import os
import warnings
from datetime import date, datetime, time, timedelta
from operator import attrgetter
from time import sleep
from typing import Set

import pytest
from typing_extensions import Literal

from lemon import api
from lemon.api import Api

API_KEY = os.getenv("API_KEY", None)


@pytest.fixture
def uut() -> Api:
    if API_KEY is None:
        warnings.warn("Please export API_KEY=your_token_here")
        pytest.fail()
    return api.create(api_token=API_KEY)


@pytest.mark.parametrize("type_", ["stock", "bond", "fund", "etf"])
@pytest.mark.e2e
def test_instruments_by_type(uut: Api, type_):
    result = uut.market_data.instruments.get(type=[type_])
    assert set(map(attrgetter("type"), result.results)) == {type_}


@pytest.mark.e2e
def test_instruments_by_search(uut: Api):
    result = uut.market_data.instruments.get(search="tesla*")
    assert len(result.results) == 3


@pytest.mark.e2e
def test_instruments_by_isin(uut: Api):
    response = uut.market_data.instruments.get(isin=["US88160R1014"])

    assert len(response.results) == 1
    assert response.results[-1].title == "TESLA INC."


@pytest.mark.parametrize("currency", ["EUR", "PLN"])
@pytest.mark.e2e
def test_instruments_by_currency(uut: Api, currency):
    response = uut.market_data.instruments.get(currency=[currency])

    given: Set[str] = set()
    for instrument in response.results:
        given.update(info.currency for info in instrument.venues)
    assert given == {currency}


@pytest.mark.parametrize("tradable", [True, False])
@pytest.mark.e2e
def test_instruments_by_tradable(uut: Api, tradable: bool):
    response = uut.market_data.instruments.get(tradable=tradable)

    given: Set[bool] = set()
    for i in response.results:
        given.update(info.tradable for info in i.venues)
    assert given == {tradable}


@pytest.mark.e2e
def test_instruments_limit(uut: Api):
    response = uut.market_data.instruments.get(limit=10)
    assert len(response.results) == 10


@pytest.mark.parametrize("period", ["m1", "h1", "d1"])
@pytest.mark.e2e
def test_ohlc_by_period(uut: Api, period: Literal["m1", "h1", "d1"]):
    isin = [
        "ANN4327C1220",
        "AT000000STR1",
        "AT00000AMAG3",
        "AT00000FACC2",
        "AT00000VIE62",
        "AT0000606306",
        "AT0000609607",
        "AT0000641352",
        "AT0000644505",
    ]

    response = uut.market_data.ohlc.get(isin=isin, period=period)

    assert 1 <= len(response.results) <= 10


@pytest.mark.e2e
def test_ohlc_by_from(uut: Api):
    # 1
    response = uut.market_data.ohlc.get(
        isin=["US88160R1014"], period="m1", from_="latest"
    )

    assert len(response.results) == 1
    ohlc = response.results[-1]

    for attr in ["o", "h", "l", "c", "v", "pbv"]:
        assert isinstance(getattr(ohlc, attr), int)

    assert isinstance(ohlc.t, datetime)

    # 2
    response = uut.market_data.ohlc.get(
        isin=["US88160R1014"], period="m1", from_=datetime.now() - timedelta(days=7)
    )

    assert len(response.results)
    ohlc = response.results[-1]

    for attr in ["o", "h", "l", "c", "v", "pbv"]:
        assert isinstance(getattr(ohlc, attr), int)


@pytest.mark.e2e
def test_ohlc_latest_by_decimals(uut: Api):
    # decimals=False
    response = uut.market_data.ohlc.get(
        isin=["US88160R1014"], period="m1", decimals=False
    )

    assert len(response.results)
    ohlc = response.results[-1]

    for attr in ["o", "h", "l", "c", "v", "pbv"]:
        assert isinstance(getattr(ohlc, attr), int), f"{attr!r} is not int"

    # decimals=True
    response = uut.market_data.ohlc.get(
        isin=["US88160R1014"], period="m1", decimals=True
    )

    assert len(response.results)
    ohlc = response.results[-1]

    for attr in ["o", "h", "l", "c", "pbv"]:
        assert isinstance(getattr(ohlc, attr), float), f"{attr!r} is not float"

    assert isinstance(ohlc.v, int)


@pytest.mark.e2e
def test_ohlc_by_epoch(uut: Api):
    # decimals=False
    response = uut.market_data.ohlc.get(isin=["US88160R1014"], period="m1", epoch=False)
    assert isinstance(response.results[-1].t, datetime)

    # decimals=True
    response = uut.market_data.ohlc.get(isin=["US88160R1014"], period="m1", epoch=True)
    assert isinstance(response.results[-1].t, int)


@pytest.mark.e2e
def test_ohlc_by_sorting(uut: Api):
    # asc
    response = uut.market_data.ohlc.get(
        isin=["US88160R1014", "US0231351067"], period="m1", sorting="asc"
    )
    assert len(response.results) == 2
    assert response.results[0].isin == "US0231351067"
    assert response.results[1].isin == "US88160R1014"

    # desc
    response = uut.market_data.ohlc.get(
        isin=["US88160R1014", "US0231351067"], period="m1", sorting="desc"
    )
    assert len(response.results) == 2
    assert response.results[0].isin == "US88160R1014"
    assert response.results[1].isin == "US0231351067"


@pytest.mark.e2e
def test_quotes_by_decimals(uut: Api):
    # decimals=False
    response = uut.market_data.quotes.get_latest(isin=["US88160R1014"], decimals=False)
    quote = response.results[-1]

    for attr in ["a", "b", "a_v", "b_v"]:
        assert isinstance(getattr(quote, attr), int), f"{attr!r} is not int"

    # decimals=True
    response = uut.market_data.quotes.get_latest(isin=["US88160R1014"], decimals=True)
    quote = response.results[-1]

    for attr in ["a_v", "b_v"]:
        assert isinstance(getattr(quote, attr), int), f"{attr!r} is not int"

    for attr in ["a", "b"]:
        assert isinstance(getattr(quote, attr), float), f"{attr!r} is not float"


@pytest.mark.e2e
def test_quotes_by_epoch(uut: Api):
    # decimals=False
    response = uut.market_data.quotes.get_latest(isin=["US88160R1014"], epoch=False)
    assert isinstance(response.results[-1].t, datetime)

    # decimals=True
    response = uut.market_data.quotes.get_latest(isin=["US88160R1014"], epoch=True)
    assert isinstance(response.results[-1].t, int)


@pytest.mark.e2e
def test_trades_by_decimals(uut: Api):
    # decimals=False
    response = uut.market_data.trades.get_latest(isin=["US88160R1014"], decimals=False)
    quote = response.results[-1]

    for attr in ["p", "v"]:
        assert isinstance(getattr(quote, attr), int), f"{attr!r} is not int"

    # decimals=True
    response = uut.market_data.trades.get_latest(isin=["US88160R1014"], decimals=True)
    quote = response.results[-1]

    assert isinstance(quote.p, float)
    assert isinstance(quote.v, int)


@pytest.mark.e2e
def test_trades_by_epoch(uut: Api):
    # decimals=False
    response = uut.market_data.trades.get_latest(isin=["US88160R1014"], epoch=False)
    assert isinstance(response.results[-1].t, datetime)

    # decimals=True
    response = uut.market_data.trades.get_latest(isin=["US88160R1014"], epoch=True)
    assert isinstance(response.results[-1].t, int)


@pytest.mark.e2e
def test_venues_by_mic(uut: Api):
    response = uut.market_data.venues.get(sorting="asc")

    assert len(response.results) == 2

    for venue in response.results:
        for i in venue.opening_days:
            assert isinstance(i, date)

        assert isinstance(venue.opening_hours.start, time)
        assert isinstance(venue.opening_hours.end, time)


@pytest.mark.e2e
def test_user_e2e(uut: Api):
    response = uut.trading.user.get()
    user = response.results

    assert user.email is not None
    assert isinstance(user.created_at, datetime)


@pytest.mark.e2e
def test_account_e2e(uut: Api):
    response = uut.trading.account.get()
    account = response.results
    assert account.created_at

    uut.trading.account.update(
        address_city="Wrocław",
        address_street_number="101",
        address_country="PL",
        address_postal_code="12345",
    )


@pytest.mark.e2e
def test_orders_e2e(uut: Api):
    # open order
    r1 = uut.trading.orders.create(
        isin="US88160R1014", side="buy", quantity=1, venue="xmun"
    )
    order_id = r1.results.id
    assert order_id is not None

    uut.trading.orders.activate(order_id)

    while 1:
        r2 = uut.trading.orders.get_order(order_id)
        if r2.results.status == "executed":
            break
        sleep(1)

    # check performance
    r3 = uut.trading.positions.get_performance(isin="US88160R1014")
    assert len(r3.results) == 1

    # fetch statements
    uut.trading.positions.get_statements(isin="US88160R1014")

    # close order
    r4 = uut.trading.orders.create(
        isin="US88160R1014", side="sell", quantity=1, venue="xmun"
    )
    order_id = r4.results.id
    assert order_id is not None

    uut.trading.orders.activate(order_id)

    while 1:
        r5 = uut.trading.orders.get_order(order_id)
        if r5.results.status == "executed":
            break
        sleep(1)

    # delete order
    r6 = uut.trading.orders.create(
        isin="US88160R1014", side="buy", quantity=1, venue="xmun"
    )
    order_id = r6.results.id
    assert order_id is not None
    uut.trading.orders.delete(order_id)
    response = uut.trading.orders.get_order(order_id)

    assert response.results.status == "canceled"
