from datetime import date, datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.positions.models import (
    GetPerformanceResponse,
    GetPositionsResponse,
    GetStatementsResponse,
    Performance,
    Position,
    Statement,
)
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

DUMMY_STATEMENTS_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "money",
    "results": [
        {
            "id": "hs_pyHJLHHNBHbK943xcyYdB8l4scC0dJs2xW",
            "order_id": "ord_pyNBHJJ66Mp9k3YHztpBb1m984WRGCYq5D",
            "external_id": None,
            "type": "order_buy",
            "quantity": 1,
            "isin": "US19260Q1076",
            "isin_title": "COINBASE GLOBAL INC.",
            "date": "2021-12-10",
            "created_at": "2021-12-10T07:57:12.628+00:00",
        },
    ],
    "previous": "https://paper-trading.lemon.markets/v1/positions/statements?limit=10&page=1",
    "next": "https://paper-trading.lemon.markets/v1/positions/statements?limit=10&page=3",
    "total": 33,
    "page": 2,
    "pages": 4,
}

DUMMY_PERFORMANCE_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "money",
    "results": [
        {
            "isin": "US19260Q1076",
            "isin_title": "COINBASE GLOBAL INC.",
            "profit": 89400,
            "loss": 0,
            "quantity_bought": 1,
            "quantity_sold": 1,
            "quantity_open": 0,
            "opened_at": "2022-02-02T16:20:30.618+00:00",
            "closed_at": "2022-02-03T12:32:00.762+00:00",
            "fees": 40000,
        },
    ],
    "previous": "https://trading.lemon.markets/v1/positions/performance?limit=10&page=1",
    "next": "https://trading.lemon.markets/v1/positions/performance?limit=10&page=3",
    "total": 37,
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

DUMMY_STATEMENTS_RESPONSE = GetStatementsResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="money",
    results=[
        Statement(
            id="hs_pyHJLHHNBHbK943xcyYdB8l4scC0dJs2xW",
            order_id="ord_pyNBHJJ66Mp9k3YHztpBb1m984WRGCYq5D",
            external_id=None,
            type="order_buy",
            quantity=1,
            isin="US19260Q1076",
            isin_title="COINBASE GLOBAL INC.",
            date=date(year=2021, month=12, day=10),
            created_at=datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
        )
    ],
    total=33,
    page=2,
    pages=4,
)

DUMMY_PERFORMANCE_RESPONSE = GetPerformanceResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="money",
    results=[
        Performance(
            isin="US19260Q1076",
            isin_title="COINBASE GLOBAL INC.",
            profit=89400,
            loss=0,
            quantity_bought=1,
            quantity_sold=1,
            quantity_open=0,
            opened_at=datetime.fromisoformat("2022-02-02T16:20:30.618+00:00"),
            closed_at=datetime.fromisoformat("2022-02-03T12:32:00.762+00:00"),
            fees=40000,
        )
    ],
    total=37,
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
        httpserver.expect_oneshot_request(
            "/positions",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_POSITIONS_PAYLOAD)
        assert (
            client.trading.positions.get(**function_kwargs) == DUMMY_POSITIONS_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/positions",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/positions",
            method="GET",
        ).respond_with_json(DUMMY_POSITIONS_PAYLOAD)

        assert client.trading.positions.get() == DUMMY_POSITIONS_RESPONSE


class TestGetStatementsApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.positions.get_statements()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/positions/statements", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"isin": "XMUN"}, "isin=XMUN"),
            (
                {"from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00")},
                "from=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            (
                {"to": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00")},
                "to=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            ({"type": "order_buy"}, "type=order_buy"),
            ({"sorting": "asc"}, "sorting=asc"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "isin": "XMUN",
                    "from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                    "to": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                    "type": "order_buy",
                    "sorting": "asc",
                    "limit": 100,
                    "page": 7,
                },
                "isin=XMUN&from=2021-11-07+22%3A59%3A00%2B00%3A00&"
                "to=2021-11-07+22%3A59%3A00%2B00%3A00&type=order_buy&sorting=asc&limit=100&page=7",
            ),
        ],
    )
    def test_get_statements(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/positions/statements",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_STATEMENTS_PAYLOAD)
        assert (
            client.trading.positions.get_statements(**function_kwargs)
            == DUMMY_STATEMENTS_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/positions/statements",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/positions/statements",
            method="GET",
        ).respond_with_json(DUMMY_STATEMENTS_PAYLOAD)

        assert client.trading.positions.get_statements() == DUMMY_STATEMENTS_RESPONSE


class TestGetPerformanceApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.positions.get_performance()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/positions/performance", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"isin": "XMUN"}, "isin=XMUN"),
            (
                {"from_": date(year=2021, month=11, day=7)},
                "from=2021-11-07",
            ),
            (
                {"to": date(year=2021, month=11, day=7)},
                "to=2021-11-07",
            ),
            ({"sorting": "asc"}, "sorting=asc"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "isin": "XMUN",
                    "from_": date(year=2021, month=11, day=7),
                    "to": date(year=2021, month=11, day=7),
                    "sorting": "asc",
                    "limit": 100,
                    "page": 7,
                },
                "isin=XMUN&from=2021-11-07&to=2021-11-07&"
                "sorting=asc&limit=100&page=7",
            ),
        ],
    )
    def test_get_performance(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/positions/performance",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_PERFORMANCE_PAYLOAD)
        assert (
            client.trading.positions.get_performance(**function_kwargs)
            == DUMMY_PERFORMANCE_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/positions/performance",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/positions/performance",
            method="GET",
        ).respond_with_json(DUMMY_PERFORMANCE_PAYLOAD)

        assert client.trading.positions.get_performance() == DUMMY_PERFORMANCE_RESPONSE
