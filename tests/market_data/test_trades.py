from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.model import GetTradesResponse, Trade
from tests.market_data.conftest import CommonMarketDataApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US19260Q1076",
            "p": 274.0,
            "pbv": 35,
            "v": 2,
            "t": "2021-10-28T09:05:14.474+00:00",
            "mic": "XMUN",
        }
    ],
    "previous": None,
    "next": None,
    "total": 1,
    "page": 1,
    "pages": 1,
}

DUMMY_PAYLOAD_WITH_EPOCH = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US19260Q1076",
            "p": 274.0,
            "pbv": 35,
            "v": 2,
            "t": 13344142,
            "mic": "XMUN",
        }
    ],
    "previous": None,
    "next": None,
    "total": 1,
    "page": 1,
    "pages": 1,
}

DUMMY_RESPONSE = GetTradesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Trade(
            isin="US19260Q1076",
            p=274,
            pbv=35,
            v=2,
            t=datetime.fromisoformat("2021-10-28T09:05:14.474+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
    next=None,
    _client=None,
)


class TestTradesApi(CommonMarketDataApiTests):
    def make_api_call(self, client: Api):
        return client.market_data.trades.get_latest(isin=["XMUN"])

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/trades/latest", "method": "GET", "query_string": "isin=XMUN"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({"isin": ["XMUN"]}, "isin=XMUN"),
            ({"isin": ["XMUN"], "mic": "XMUN"}, "isin=XMUN&mic=XMUN"),
            ({"isin": ["XMUN"], "decimals": False}, "isin=XMUN&decimals=False"),
            ({"isin": ["XMUN"], "epoch": False}, "isin=XMUN&epoch=False"),
            ({"isin": ["XMUN"], "sorting": "asc"}, "isin=XMUN&sorting=asc"),
            ({"isin": ["XMUN"], "limit": 100}, "isin=XMUN&limit=100"),
            ({"isin": ["XMUN"], "page": 3}, "isin=XMUN&page=3"),
            (
                {
                    "isin": ["XMUN"],
                    "mic": "XMUN",
                    "decimals": False,
                    "epoch": False,
                    "sorting": "asc",
                    "limit": 100,
                    "page": 3,
                },
                "isin=XMUN&mic=XMUN&decimals=False&"
                "epoch=False&sorting=asc&limit=100&page=3",
            ),
        ],
    )
    def test_get_trades(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        DUMMY_RESPONSE._client = client.market_data

        assert client.market_data.trades.get_latest(**function_kwargs) == DUMMY_RESPONSE

    def test_get_trades_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string="isin=XMUN&decimals=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        trade = client.market_data.trades.get_latest(
            isin=["XMUN"], decimals=True
        ).results[0]

        assert isinstance(trade.p, float)
        assert isinstance(trade.pbv, float)

    def test_get_trades_non_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string="isin=XMUN&decimals=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        trade = client.market_data.trades.get_latest(
            isin=["XMUN"], decimals=False
        ).results[0]

        assert isinstance(trade.p, int)
        assert isinstance(trade.pbv, int)

    def test_get_trades_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string="isin=XMUN&epoch=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD_WITH_EPOCH)

        trade = client.market_data.trades.get_latest(isin=["XMUN"], epoch=True).results[
            0
        ]

        assert isinstance(trade.t, int)

    def test_get_trades_non_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string="isin=XMUN&epoch=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        trade = client.market_data.trades.get_latest(
            isin=["XMUN"], epoch=False
        ).results[0]

        assert isinstance(trade.t, datetime)

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string="isin=XMUN",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/trades/latest",
            query_string="isin=XMUN",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        DUMMY_RESPONSE._client = client.market_data

        assert client.market_data.trades.get_latest(isin=["XMUN"]) == DUMMY_RESPONSE
