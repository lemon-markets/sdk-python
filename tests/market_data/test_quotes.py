import abc
from datetime import datetime, timezone
from urllib.parse import urlencode

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.model import GetQuotesResponse, Quote
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
    _client=None,
    next=None,
)


class BaseQuotesAPITests(CommonMarketDataApiTests):
    @property
    @abc.abstractmethod
    def uri(self) -> str:
        ...

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": self.uri, "method": "GET", "query_string": "isin=A"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({"isin": ["A"]}, "isin=A"),
            ({"isin": ["A"], "mic": "XMUN"}, "isin=A&mic=XMUN"),
            ({"isin": ["A"], "decimals": False}, "isin=A&decimals=False"),
            ({"isin": ["A"], "epoch": False}, "isin=A&epoch=False"),
            ({"isin": ["A"], "sorting": "asc"}, "isin=A&sorting=asc"),
            ({"isin": ["A"], "limit": 100}, "isin=A&limit=100"),
            ({"isin": ["A"], "page": 3}, "isin=A&page=3"),
            (
                {
                    "isin": ["A"],
                    "mic": "XMUN",
                    "decimals": False,
                    "epoch": False,
                    "sorting": "asc",
                    "limit": 100,
                    "page": 3,
                },
                "isin=A&mic=XMUN&decimals=False&"
                "epoch=False&sorting=asc&limit=100&page=3",
            ),
        ],
    )
    def test_get_quotes(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        DUMMY_RESPONSE._client = client.market_data

        assert self.make_api_call(client, **function_kwargs) == DUMMY_RESPONSE

    def test_get_quotes_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string="isin=A&decimals=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        quote = self.make_api_call(client, decimals=True).results[0]
        assert isinstance(quote.b, float)
        assert isinstance(quote.a, float)

    def test_get_quotes_non_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string="isin=A&decimals=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        quote = self.make_api_call(client, decimals=False).results[0]
        assert isinstance(quote.b, int)
        assert isinstance(quote.a, int)

    def test_get_quotes_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string="isin=A&epoch=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD_WITH_EPOCH)

        quote = self.make_api_call(client, epoch=True).results[0]
        assert isinstance(quote.t, int)

    def test_get_quotes_non_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string="isin=A&epoch=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        quote = self.make_api_call(client, epoch=False).results[0]
        assert isinstance(quote.t, datetime)

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string="isin=A",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            self.uri,
            query_string="isin=A",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        DUMMY_RESPONSE._client = client.market_data
        assert self.make_api_call(client) == DUMMY_RESPONSE


class TestGetLatestQuotes(BaseQuotesAPITests):
    @property
    def uri(self):
        return "/quotes/latest"

    def make_api_call(self, client: Api, **kwargs):
        data = {"isin": ["A"]}
        data.update(kwargs)
        return client.market_data.quotes.get_latest(**data)


DT = datetime(2001, 2, 3, 4, 5, 6, tzinfo=timezone.utc)


class TestGetQuotes(BaseQuotesAPITests):
    @property
    def uri(self):
        return "/quotes"

    def make_api_call(self, client: Api, **kwargs):
        data = {"isin": "A"}
        data.update(kwargs)
        return client.market_data.quotes.get(**data)

    @pytest.mark.parametrize(
        "function_kwargs,query_params",
        [
            ({"isin": "A", "from_": DT}, {"isin": "A", "from": DT}),
            ({"isin": "A", "to": DT}, {"isin": "A", "to": DT}),
            ({"isin": "A", "to": 2}, {"isin": "A", "to": "P2D"}),
        ],
    )
    def test_getting_quotes_range(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_params
    ):
        httpserver.expect_oneshot_request(
            self.uri,
            query_string=urlencode(query_params),
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        DUMMY_RESPONSE._client = client.market_data
        assert self.make_api_call(client, **function_kwargs) == DUMMY_RESPONSE
