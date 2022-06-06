from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.instruments.models import (
    GetInstrumentsResponse,
    Instrument,
    Venue,
)
from tests.market_data.conftest import CommonMarketDataApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US19260Q1076",
            "wkn": "A2QP7J",
            "name": "COINBASE GLB.CL.A -,00001",
            "title": "COINBASE GLOBAL INC",
            "symbol": "1QZ",
            "type": "stock",
            "venues": [
                {
                    "name": "Börse München - Gettex",
                    "title": "Gettex",
                    "mic": "XMUN",
                    "is_open": True,
                    "tradable": True,
                    "currency": "EUR",
                }
            ],
        }
    ],
    "previous": "https://data.lemon.markets/v1/instruments/?limit=100&page=1",
    "next": "https://data.lemon.markets/v1/instruments/?limit=100&page=3",
    "total": 26283,
    "page": 2,
    "pages": 263,
}

DUMMY_RESPONSE = GetInstrumentsResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Instrument(
            isin="US19260Q1076",
            wkn="A2QP7J",
            name="COINBASE GLB.CL.A -,00001",
            title="COINBASE GLOBAL INC",
            symbol="1QZ",
            type="stock",
            venues=[
                Venue(
                    name="Börse München - Gettex",
                    title="Gettex",
                    mic="XMUN",
                    is_open=True,
                    tradable=True,
                    currency="EUR",
                )
            ],
        )
    ],
    total=26283,
    page=2,
    pages=263,
)


class TestInstrumentsApi(CommonMarketDataApiTests):
    def make_api_call(self, client: Api):
        return client.market_data.instruments.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/instruments", "method": "GET"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"isin": ["XMUN"]}, "isin=XMUN"),
            ({"search": "foo"}, "search=foo"),
            ({"type": ["stock", "etf"]}, "type=stock&type=etf"),
            ({"mic": ["XMUN"]}, "mic=XMUN"),
            ({"currency": "USD"}, "currency=USD"),
            ({"tradable": False}, "tradable=False"),
            ({"sorting": "asc"}, "sorting=asc"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "isin": ["XMUN"],
                    "search": "foo",
                    "type": ["stock", "etf"],
                    "mic": ["XMUN"],
                    "currency": "USD",
                    "tradable": False,
                    "sorting": "asc",
                    "limit": 100,
                    "page": 7,
                },
                "isin=XMUN&search=foo&type=stock&type=etf&mic=XMUN&"
                "currency=USD&tradable=False&sorting=asc&limit=100&page=7",
            ),
        ],
    )
    def test_get_instruments(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/instruments",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert client.market_data.instruments.get(**function_kwargs) == DUMMY_RESPONSE

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/instruments",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/instruments",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        assert client.market_data.instruments.get() == DUMMY_RESPONSE
