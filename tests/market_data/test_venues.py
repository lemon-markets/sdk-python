from datetime import date, datetime, time

import pytest
import pytz
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.market_data.model import GetVenuesResponse, OpeningHours, Venue
from tests.market_data.conftest import CommonMarketDataApiTests

DUMMY_PAYLOAD = {
    "time": "2022-02-14T20:44:03.759+00:00",
    "results": [
        {
            "name": "Börse München - Gettex",
            "title": "Gettex",
            "mic": "XMUN",
            "is_open": True,
            "opening_hours": {
                "start": "08:00",
                "end": "22:00",
                "timezone": "Europe/Berlin",
            },
            "opening_days": ["2021-12-06", "2021-12-07", "2021-12-08"],
        }
    ],
    "previous": "https://data.lemon.markets/v1/venues/?limit=1&&page=1",
    "next": "https://data.lemon.markets/v1/venues/?limit=1&&page=3",
    "total": 3,
    "page": 2,
    "pages": 3,
}

DUMMY_RESPONSE = GetVenuesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Venue(
            name="Börse München - Gettex",
            title="Gettex",
            mic="XMUN",
            is_open=True,
            opening_hours=OpeningHours(
                start=time(
                    hour=8,
                    minute=0,
                    tzinfo=pytz.timezone("Europe/Berlin"),
                ),
                end=time(
                    hour=22,
                    minute=0,
                    tzinfo=pytz.timezone("Europe/Berlin"),
                ),
            ),
            opening_days=[
                date(year=2021, month=12, day=6),
                date(year=2021, month=12, day=7),
                date(year=2021, month=12, day=8),
            ],
        )
    ],
    total=3,
    page=2,
    pages=3,
)


class TestVenuesApi(CommonMarketDataApiTests):
    def make_api_call(self, client: Api):
        return client.market_data.venues.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/venues", "method": "GET"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"mic": "XMUN"}, "mic=XMUN"),
            ({"sorting": "asc"}, "sorting=asc"),
            ({"limit": 100}, "limit=100"),
            ({"page": 2}, "page=2"),
            ({"mic": "XMUN", "limit": 100, "page": 2}, "mic=XMUN&limit=100&page=2"),
        ],
    )
    def test_get_venues(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/venues",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)
        assert client.market_data.venues.get(**function_kwargs) == DUMMY_RESPONSE

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/venues",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/venues",
            method="GET",
        ).respond_with_json(DUMMY_PAYLOAD)

        assert client.market_data.venues.get() == DUMMY_RESPONSE
