from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.positions.models import GetPositionsResponse, Position
from tests.conftest import CommonApiTests

DUMMY_POSITIONS_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "paper",
    "results": [
        {
            "isin": "US19260Q1076",
            "isin_title": "COINBASE GLOBAL INC.",
            "quantity": 2,
            "buy_price_avg": 2965000,
            "estimated_price_total": 5800000,
            "estimated_price": 2900000,
        },
    ],
    "previous": "https://paper-trading.lemon.markets/v1/positions/?limit=10&page=1",
    "next": "https://paper-trading.lemon.markets/v1/positions/?limit=10&page=3",
    "total": 33,
    "page": 2,
    "pages": 4,
}

DUMMY_POSITIONS_RESPONSE = GetPositionsResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
    results=[
        Position(
            isin="US19260Q1076",
            isin_title="COINBASE GLOBAL INC.",
            quantity=2,
            buy_price_avg=2965000,
            estimated_price_total=5800000,
            estimated_price=2900000,
        )
    ],
    total=33,
    page=2,
    pages=4,
)


class TestGetPositionsApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.positions.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/positions", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"isin": "XMUN"}, "isin=XMUN"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "isin": "XMUN",
                    "limit": 100,
                    "page": 7,
                },
                "isin=XMUN&limit=100&page=7",
            ),
        ],
    )
    def test_get_positions(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_request(
            "/positions",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_POSITIONS_PAYLOAD)
        assert (
            client.trading.positions.get(**function_kwargs) == DUMMY_POSITIONS_RESPONSE
        )
