from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.quotes.models import GetQuotesResponse, Quote
from tests.conftest import CommonApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US88160R1014",
            "b_v": 87,
            "a_v": 87,
            "b": 921.1,
            "a": 921.1,
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

DUMMY_RESPONSE = GetQuotesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Quote(
            isin="US88160R1014",
            b_v=87,
            a_v=87,
            b=921.1,
            a=921.1,
            t=datetime.fromisoformat("2021-10-28T08:51:03.669+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
)


class TestQuotesApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.market_data.quotes.get(isin=["XMUN"])

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/quotes/latest", "method": "GET", "query_string": "isin=XMUN"}

    @pytest.fixture
    def httpserver(self, market_data_httpserver: HTTPServer):
        return market_data_httpserver

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({"isin": ["XMUN"]}, "isin=XMUN"),
            ({"isin": ["XMUN"], "mic": "XMUN"}, "isin=XMUN&mic=XMUN"),
            ({"isin": ["XMUN"], "from_": "now"}, "isin=XMUN&from=now"),
            ({"isin": ["XMUN"], "decimals": True}, "isin=XMUN&decimals=True"),
            ({"isin": ["XMUN"], "epoch": False}, "isin=XMUN&epoch=False"),
            ({"isin": ["XMUN"], "sorting": "asc"}, "isin=XMUN&sorting=asc"),
            ({"isin": ["XMUN"], "limit": 100}, "isin=XMUN&limit=100"),
            ({"isin": ["XMUN"], "page": 3}, "isin=XMUN&page=3"),
            (
                {
                    "isin": ["XMUN"],
                    "mic": "XMUN",
                    "from_": "now",
                    "decimals": True,
                    "epoch": False,
                    "sorting": "asc",
                    "limit": 100,
                    "page": 3,
                },
                "isin=XMUN&mic=XMUN&from=now&decimals=True&"
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
        assert client.market_data.quotes.get(**function_kwargs) == DUMMY_RESPONSE

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

        assert client.market_data.quotes.get(isin=["XMUN"]) == DUMMY_RESPONSE
