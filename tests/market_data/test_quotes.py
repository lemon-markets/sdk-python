from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.quotes.models import GetQuotesResponse, Quote
from tests.market_data.conftest import CommonMarketDataApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US88160R1014",
            "b_v": 87,
            "a_v": 87,
            "b": 921,
            "a": 921,
            "t": "2021-10-28T08:51:03.669+00:00",
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
            "isin": "US88160R1014",
            "b_v": 87,
            "a_v": 87,
            "b": 921,
            "a": 921,
            "t": 11241521,
            "mic": "XMUN",
        }
    ],
    "previous": None,
    "next": None,
    "total": 1,
    "page": 1,
    "pages": 1,
}

DUMMY_RESPONSE = GetQuotesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Quote(
            isin="US88160R1014",
            b_v=87,
            a_v=87,
            b=921,
            a=921,
            t=datetime.fromisoformat("2021-10-28T08:51:03.669+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
)


class TestQuotesApi(CommonMarketDataApiTests):
    def make_api_call(self, client: Api):
        return client.market_data.quotes.get_latest(isin=["XMUN"])

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/quotes/latest", "method": "GET", "query_string": "isin=XMUN"}

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
    def test_get_quotes(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert client.market_data.quotes.get_latest(**function_kwargs) == DUMMY_RESPONSE

    def test_get_quotes_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string="isin=XMUN&decimals=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        quote = client.market_data.quotes.get_latest(
            isin=["XMUN"], decimals=True
        ).results[0]

        assert isinstance(quote.b, float)
        assert isinstance(quote.a, float)

    def test_get_quotes_non_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string="isin=XMUN&decimals=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        quote = client.market_data.quotes.get_latest(
            isin=["XMUN"], decimals=False
        ).results[0]

        assert isinstance(quote.b, int)
        assert isinstance(quote.a, int)

    def test_get_quotes_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string="isin=XMUN&epoch=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD_WITH_EPOCH)

        quote = client.market_data.quotes.get_latest(isin=["XMUN"], epoch=True).results[
            0
        ]

        assert isinstance(quote.t, int)

    def test_get_quotes_non_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string="isin=XMUN&epoch=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        quote = client.market_data.quotes.get_latest(
            isin=["XMUN"], epoch=False
        ).results[0]

        assert isinstance(quote.t, datetime)

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string="isin=XMUN",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/quotes/latest",
            query_string="isin=XMUN",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        assert client.market_data.quotes.get_latest(isin=["XMUN"]) == DUMMY_RESPONSE
