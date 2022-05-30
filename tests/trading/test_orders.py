from datetime import date, datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.orders.models import (
    CreatedOrder,
    CreateOrderResponse,
    GetOrdersResponse,
    Order,
    RegulatoryInformation,
)
from tests.conftest import CommonApiTests

DUMMY_ORDERS_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "paper",
    "results": [
        {
            "id": "ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
            "isin": "DE0008232125",
            "isin_title": "DEUTSCHE LUFTHANSA AG",
            "expires_at": "2021-11-07T22:59:00.000+00:00",
            "created_at": "2021-11-04T12:25:30.063+00:00",
            "side": "buy",
            "quantity": 1000,
            "stop_price": None,
            "limit_price": None,
            "estimated_price": 66140000,
            "estimated_price_total": 66140000,
            "venue": "xmun",
            "status": "inactive",
            "type": "market",
            "executed_quantity": 1,
            "executed_price": 2965000,
            "executed_price_total": 2965000,
            "executed_at": "2021-11-04T12:25:12.402+00:00",
            "rejected_at": None,
            "notes": "My Notes",
            "charge": 20000,
            "chargeable_at": "2021-12-10T07:57:12.628+00:00",
            "key_creation_id": "apk_pyJHHbbDDNympXsVwZzPp2nNBlTMTLRmxy",
            "key_activation_id": "apk_pyJHHbbDDNympXsVwZzPp2nNBlTMTLRmxy",
            "regulatory_information": {
                "costs_entry": 20000,
                "costs_entry_pct": "0.30%",
                "costs_running": 0,
                "costs_running_pct": "0.00%",
                "costs_product": 0,
                "costs_product_pct": "0.00%",
                "costs_exit": 20000,
                "costs_exit_pct": "0.30%",
                "yield_reduction_year": 20000,
                "yield_reduction_year_pct": "0.30%",
                "yield_reduction_year_following": 0,
                "yield_reduction_year_following_pct": "0.00%",
                "yield_reduction_year_exit": 20000,
                "yield_reduction_year_exit_pct": "0.30%",
                "estimated_holding_duration_years": "5",
                "estimated_yield_reduction_total": 40000,
                "estimated_yield_reduction_total_pct": "0.61%",
                "KIID": "text",
                "legal_disclaimer": "text",
            },
            "idempotency": "1235abcd",
        }
    ],
    "previous": "https://paper-trading.lemon.markets/v1/orders/?limit=10&page=1",
    "next": "https://paper-trading.lemon.markets/v1/orders/?limit=10&page=3",
    "total": 33,
    "page": 2,
    "pages": 4,
}

DUMMY_ORDER_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "paper",
    "results": {
        "created_at": "2021-11-15T13:58:19.981+00:00",
        "id": "ord_pyPGQggmmj0jhlLHw2nfM92Hm9PmgTYq9K",
        "status": "inactive",
        "regulatory_information": {
            "costs_entry": 20000,
            "costs_entry_pct": "0.30%",
            "costs_running": 0,
            "costs_running_pct": "0.00%",
            "costs_product": 0,
            "costs_product_pct": "0.00%",
            "costs_exit": 20000,
            "costs_exit_pct": "0.30%",
            "yield_reduction_year": 20000,
            "yield_reduction_year_pct": "0.30%",
            "yield_reduction_year_following": 0,
            "yield_reduction_year_following_pct": "0.00%",
            "yield_reduction_year_exit": 20000,
            "yield_reduction_year_exit_pct": "0.30%",
            "estimated_holding_duration_years": "5",
            "estimated_yield_reduction_total": 40000,
            "estimated_yield_reduction_total_pct": "0.61%",
            "KIID": "text",
            "legal_disclaimer": "text",
        },
        "isin": "DE0008232125",
        "expires_at": "2021-11-07T22:59:00.000+00:00",
        "side": "buy",
        "quantity": 1,
        "stop_price": None,
        "limit_price": None,
        "venue": "xmun",
        "estimated_price": 66140000,
        "notes": "I want to attach a note to this order",
        "idempotency": "1234abcd",
        "charge": 20000,
        "chargeable_at": "2021-12-10T07:57:12.628+00:00",
        "key_creation_id": "apk_pyJKKbbDDNympXsVwZzPp2nBVlTMTLRmxy",
    },
}


DUMMY_ORDERS_RESPONSE = GetOrdersResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
    results=[
        Order(
            id="ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
            isin="DE0008232125",
            isin_title="DEUTSCHE LUFTHANSA AG",
            expires_at=datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
            created_at=datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
            side="buy",
            quantity=1000,
            stop_price=None,
            limit_price=None,
            estimated_price=66140000,
            estimated_price_total=66140000,
            venue="xmun",
            status="inactive",
            type="market",
            executed_quantity=1,
            executed_price=2965000,
            executed_price_total=2965000,
            executed_at=datetime.fromisoformat("2021-11-04T12:25:12.402+00:00"),
            rejected_at=None,
            notes="My Notes",
            charge=20000,
            chargeable_at=datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
            key_creation_id="apk_pyJHHbbDDNympXsVwZzPp2nNBlTMTLRmxy",
            key_activation_id="apk_pyJHHbbDDNympXsVwZzPp2nNBlTMTLRmxy",
            regulatory_information=RegulatoryInformation(
                costs_entry=20000,
                costs_entry_pct="0.30%",
                costs_running=0,
                costs_running_pct="0.00%",
                costs_product=0,
                costs_product_pct="0.00%",
                costs_exit=20000,
                costs_exit_pct="0.30%",
                yield_reduction_year=20000,
                yield_reduction_year_pct="0.30%",
                yield_reduction_year_following=0,
                yield_reduction_year_following_pct="0.00%",
                yield_reduction_year_exit=20000,
                yield_reduction_year_exit_pct="0.30%",
                estimated_holding_duration_years="5",
                estimated_yield_reduction_total=40000,
                estimated_yield_reduction_total_pct="0.61%",
                KIID="text",
                legal_disclaimer="text",
            ),
            idempotency="1235abcd",
        )
    ],
    total=33,
    page=2,
    pages=4,
)

DUMMY_ORDER_RESPONSE = CreateOrderResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
    results=CreatedOrder(
        id="ord_pyPGQggmmj0jhlLHw2nfM92Hm9PmgTYq9K",
        created_at=datetime.fromisoformat("2021-11-15T13:58:19.981+00:00"),
        status="inactive",
        regulatory_information=RegulatoryInformation(
            costs_entry=20000,
            costs_entry_pct="0.30%",
            costs_running=0,
            costs_running_pct="0.00%",
            costs_product=0,
            costs_product_pct="0.00%",
            costs_exit=20000,
            costs_exit_pct="0.30%",
            yield_reduction_year=20000,
            yield_reduction_year_pct="0.30%",
            yield_reduction_year_following=0,
            yield_reduction_year_following_pct="0.00%",
            yield_reduction_year_exit=20000,
            yield_reduction_year_exit_pct="0.30%",
            estimated_holding_duration_years="5",
            estimated_yield_reduction_total=40000,
            estimated_yield_reduction_total_pct="0.61%",
            KIID="text",
            legal_disclaimer="text",
        ),
        isin="DE0008232125",
        expires_at=datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
        side="buy",
        quantity=1,
        stop_price=None,
        limit_price=None,
        venue="xmun",
        estimated_price=66140000,
        notes="I want to attach a note to this order",
        idempotency="1234abcd",
        charge=20000,
        chargeable_at=datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
        key_creation_id="apk_pyJKKbbDDNympXsVwZzPp2nBVlTMTLRmxy",
    ),
)


class TestGetOrdersApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/orders", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            (
                {"from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00")},
                "from=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            (
                {"to": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00")},
                "to=2021-11-07+22%3A59%3A00%2B00%3A00",
            ),
            ({"isin": "XMUN"}, "isin=XMUN"),
            ({"side": "sell"}, "side=sell"),
            ({"status": "inactive"}, "status=inactive"),
            ({"type": "market"}, "type=market"),
            ({"key_creation_id": "foo"}, "key_creation_id=foo"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "from_": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                    "to": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
                    "isin": "XMUN",
                    "side": "sell",
                    "status": "inactive",
                    "type": "market",
                    "key_creation_id": "foo",
                    "limit": 100,
                    "page": 7,
                },
                "from=2021-11-07+22%3A59%3A00%2B00%3A00&to=2021-11-07+22%3A59%3A00%2B00%3A00&"
                "isin=XMUN&side=sell&status=inactive&type=market&key_creation_id=foo&limit=100&"
                "page=7",
            ),
        ],
    )
    def test_get_orders(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_request(
            "/orders",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_ORDERS_PAYLOAD)
        assert client.trading.orders.get(**function_kwargs) == DUMMY_ORDERS_RESPONSE


class TestCreateOrderApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.create(
            isin="DE0008232125",
            expires_at=date(year=2021, month=11, day=7),
            side="buy",
            quantity=1000,
            venue="xmun",
        )

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/orders",
            "method": "POST",
            "json": {
                "isin": "DE0008232125",
                "expires_at": "2021-11-07",
                "side": "buy",
                "quantity": 1000,
                "venue": "xmun",
                "stop_price": None,
                "limit_price": None,
                "notes": None,
                "idempotency": None,
            },
        }

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    def test_create_order(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_request(
            "/orders",
            method="POST",
            json={
                "isin": "DE0008232125",
                "expires_at": "2021-11-07",
                "side": "buy",
                "quantity": 1000,
                "venue": "xmun",
                "stop_price": 1000,
                "limit_price": 500,
                "notes": "foo",
                "idempotency": "bar",
            },
        ).respond_with_json(DUMMY_ORDER_PAYLOAD)
        assert (
            client.trading.orders.create(
                isin="DE0008232125",
                expires_at=date(year=2021, month=11, day=7),
                side="buy",
                quantity=1000,
                venue="xmun",
                stop_price=1000,
                limit_price=500,
                notes="foo",
                idempotency="bar",
            )
            == DUMMY_ORDER_RESPONSE
        )
