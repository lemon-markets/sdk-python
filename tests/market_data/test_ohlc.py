from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.ohlc.models import GetOhlcResponse, OhlcData
from tests.conftest import CommonApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "isin": "US88160R1014",
            "o": 777.9,
            "h": 777.9,
            "l": 762.5,
            "c": 768.7,
            "v": 433,
            "pbv": 333645.1,
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

DUMMY_RESPONSE = GetOhlcResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        OhlcData(
            isin="US88160R1014",
            o=777.9,
            h=777.9,
            l=762.5,
            c=768.7,
            v=433,
            pbv=333645.1,
            t=datetime.fromisoformat("2021-09-02T00:00:00.000+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
)


class TestOhlcApi(CommonApiTests):
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
            ({"isin": ["XMUN"], "mic": "XMUN"}, "mic=XMUN&isin=XMUN"),
            ({"isin": ["XMUN"], "from_": "now"}, "isin=XMUN&from=now"),
            ({"isin": ["XMUN"], "to": "now"}, "isin=XMUN&to=now"),
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
                    "to": "now",
                    "decimals": True,
                    "epoch": False,
                    "sorting": "asc",
                    "limit": 100,
                    "page": 3,
                },
                "mic=XMUN&isin=XMUN&from=now&to=now&decimals=True&"
                "epoch=False&sorting=asc&limit=100&page=3",
            ),
        ],
    )
    def test_get_ohlc(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string, period
    ):
        httpserver.expect_request(
            f"/ohlc/{period}",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert (
            client.market_data.ohlc.get(period=period, **function_kwargs)
            == DUMMY_RESPONSE
        )
