from datetime import datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.orders.models import GetOrdersResponse, Order, RegulatoryInformation
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


class TestGetOrdersApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/orders", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    def test_get_orders(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_request(
            "/orders",
            method="GET",
        ).respond_with_json(DUMMY_ORDERS_PAYLOAD)
        assert client.trading.orders.get() == DUMMY_ORDERS_RESPONSE
