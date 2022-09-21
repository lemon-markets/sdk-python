from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.model import GetOhlcResponse, OhlcData
from tests.market_data.conftest import CommonMarketDataApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US88160R1014",
            "o": 777,
            "h": 777,
            "l": 762,
            "c": 768,
            "v": 433,
            "pbv": 333645,
            "t": "2021-09-02T00:00:00.000+00:00",
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
            "o": 777,
            "h": 777,
            "l": 762,
            "c": 768,
            "v": 433,
            "pbv": 333645,
            "t": 1045643,
            "mic": "XMUN",
        }
    ],
    "previous": None,
    "next": None,
    "total": 1,
    "page": 1,
    "pages": 1,
}

DUMMY_RESPONSE = GetOhlcResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        OhlcData(
            isin="US88160R1014",
            o=777,
            h=777,
            l=762,
            c=768,
            v=433,
            pbv=333645,
            t=datetime.fromisoformat("2021-09-02T00:00:00.000+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
)


class TestGetOhlcApi(CommonMarketDataApiTests):
    def make_api_call(self, client: Api):
        return client.market_data.ohlc.get(period="d1", isin=["XMUN"])

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/ohlc/d1", "method": "GET", "query_string": "isin=XMUN"}

    @pytest.mark.parametrize("period", ["h1", "d1", "m1"])
    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({"isin": ["XMUN"]}, "isin=XMUN"),
            ({"isin": ["XMUN"], "mic": "XMUN"}, "isin=XMUN&mic=XMUN"),
            (
                {
                    "isin": ["XMUN"],
                    "from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                },
                "isin=XMUN&from=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            (
                {
                    "isin": ["XMUN"],
                    "to": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                },
                "isin=XMUN&to=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            ({"isin": ["XMUN"], "decimals": False}, "isin=XMUN&decimals=False"),
            ({"isin": ["XMUN"], "epoch": False}, "isin=XMUN&epoch=False"),
            ({"isin": ["XMUN"], "sorting": "asc"}, "isin=XMUN&sorting=asc"),
            ({"isin": ["XMUN"], "limit": 100}, "isin=XMUN&limit=100"),
            ({"isin": ["XMUN"], "page": 3}, "isin=XMUN&page=3"),
            (
                {
                    "isin": ["XMUN"],
                    "mic": "XMUN",
                    "from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                    "to": 7,
                    "decimals": False,
                    "epoch": False,
                    "sorting": "asc",
                    "limit": 100,
                    "page": 3,
                },
                "isin=XMUN&mic=XMUN&from=2021-11-07+22%3A59%3A00%2B00%3A00&to=P7D&decimals=False&"
                "epoch=False&sorting=asc&limit=100&page=3",
            ),
        ],
    )
    def test_get_ohlc(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string, period
    ):
        httpserver.expect_oneshot_request(
            f"/ohlc/{period}",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert (
            client.market_data.ohlc.get(period=period, **function_kwargs)
            == DUMMY_RESPONSE
        )

    @pytest.mark.parametrize("period", ["h1", "d1", "m1"])
    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({"isin": ["XMUN"]}, "isin=XMUN"),
            ({"isin": ["XMUN"], "mic": "XMUN"}, "isin=XMUN&mic=XMUN"),
            (
                {
                    "isin": ["XMUN"],
                    "from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                },
                "isin=XMUN&from=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            (
                {
                    "isin": ["XMUN"],
                    "to": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                },
                "isin=XMUN&to=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            ({"isin": ["XMUN"], "decimals": False}, "isin=XMUN&decimals=False"),
            ({"isin": ["XMUN"], "epoch": False}, "isin=XMUN&epoch=False"),
            ({"isin": ["XMUN"], "sorting": "asc"}, "isin=XMUN&sorting=asc"),
            ({"isin": ["XMUN"], "limit": 100}, "isin=XMUN&limit=100"),
            (
                {
                    "isin": ["XMUN"],
                    "mic": "XMUN",
                    "from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                    "to": 7,
                    "decimals": False,
                    "epoch": False,
                    "sorting": "asc",
                    "limit": 100,
                },
                "isin=XMUN&mic=XMUN&from=2021-11-07+22%3A59%3A00%2B00%3A00&to=P7D&decimals=False&"
                "epoch=False&sorting=asc&limit=100",
            ),
        ],
    )
    def test_iter_ohlc(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string, period
    ):
        httpserver.expect_oneshot_request(
            f"/ohlc/{period}",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert (
            list(client.market_data.ohlc.iter(period=period, **function_kwargs))
            == DUMMY_RESPONSE.results
        )

    def test_get_ohlc_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/ohlc/m1",
            query_string="isin=XMUN&decimals=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        ohlc = client.market_data.ohlc.get("m1", isin=["XMUN"], decimals=True).results[
            0
        ]

        assert isinstance(ohlc.o, float)
        assert isinstance(ohlc.h, float)
        assert isinstance(ohlc.l, float)
        assert isinstance(ohlc.c, float)
        assert isinstance(ohlc.pbv, float)

    def test_get_ohlc_non_decimal_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/ohlc/m1",
            query_string="isin=XMUN&decimals=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        ohlc = client.market_data.ohlc.get("m1", isin=["XMUN"], decimals=False).results[
            0
        ]

        assert isinstance(ohlc.o, int)
        assert isinstance(ohlc.h, int)
        assert isinstance(ohlc.l, int)
        assert isinstance(ohlc.c, int)
        assert isinstance(ohlc.pbv, int)

    def test_get_ohlc_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/ohlc/m1",
            query_string="isin=XMUN&epoch=True",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD_WITH_EPOCH)

        ohlc = client.market_data.ohlc.get("m1", isin=["XMUN"], epoch=True).results[0]

        assert isinstance(ohlc.t, int)

    def test_get_ohlc_non_epoch_form(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/ohlc/m1",
            query_string="isin=XMUN&epoch=False",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        ohlc = client.market_data.ohlc.get("m1", isin=["XMUN"], epoch=False).results[0]

        assert isinstance(ohlc.t, datetime)

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/ohlc/h1",
            query_string="isin=XMUN",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/ohlc/h1",
            query_string="isin=XMUN",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        assert client.market_data.ohlc.get(period="h1", isin=["XMUN"]) == DUMMY_RESPONSE

    def test_raise_on_invalid_input(self, client: Api):
        with pytest.raises(ValueError):
            client.market_data.ohlc.get(period="", isin=["XMUN"])  # type: ignore
