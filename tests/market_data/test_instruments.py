from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import LemonApi
from lemon.market_data.instruments.models import (
    GetInstrumentsResponse,
    Instrument,
    Venue,
)
from tests.conftest import CommonApiTests, build_query_matcher

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
    result=[
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


class TestVenuesApi(CommonApiTests):
    def make_api_call(self, client: LemonApi):
        return client.market_data.instruments.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/instruments", "method": "GET"}

    @pytest.mark.parametrize(
        "function_kwargs",
        [
            {},
            {"isin": ["XMUN"]},
            {"search": "foo"},
            {"type": ["stock", "etf"]},
            {"mic": ["XMUN"]},
            {"currency": "USD"},
            {"tradable": False},
            {"sorting": "asc"},
            {"limit": 100},
            {"page": 7},
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
        ],
    )
    def test_get_instruments(
        self, client: LemonApi, httpserver: HTTPServer, function_kwargs
    ):
        httpserver.expect_request(
            "/instruments",
            query_string=build_query_matcher(function_kwargs),
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert client.market_data.instruments.get(**function_kwargs) == DUMMY_RESPONSE
