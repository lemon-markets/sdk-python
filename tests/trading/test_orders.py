from datetime import date, datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.model import (
    ActivateOrderResponse,
    CreatedOrder,
    CreateOrderResponse,
    DeleteOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    Order,
    RegulatoryInformation,
)
from tests.trading.conftest import CommonTradingApiTests

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
            "activated_at": "2021-11-04T12:25:30.063+00:00",
            "cancelled_at": "2021-11-04T12:25:30.063+00:00",
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
    "t": "https://paper-trading.lemon.markets/v1/orders/?limit=10&page=3",
    "total": 33,
    "page": 2,
    "pages": 4,
}

DUMMY_CREATE_ORDER_PAYLOAD = {
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
        "estimated_price_total": 66140000,
        "notes": "I want to attach a note to this order",
        "idempotency": "1234abcd",
        "charge": 20000,
        "chargeable_at": "2021-12-10T07:57:12.628+00:00",
        "key_creation_id": "apk_pyJKKbbDDNympXsVwZzPp2nBVlTMTLRmxy",
    },
}

DUMMY_ACTIVATE_ORDER_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "mode": "paper",
    "status": "ok",
}

DUMMY_ORDER_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "paper",
    "results": {
        "id": "ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
        "isin": "DE0008232125",
        "isin_title": "DEUTSCHE LUFTHANSA AG",
        "expires_at": "2021-11-07T22:59:00.000+00:00",
        "created_at": "2021-11-04T12:25:30.063+00:00",
        "activated_at": "2021-11-04T12:25:30.063+00:00",
        "cancelled_at": "2021-11-04T12:25:30.063+00:00",
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
        "idempotency": "1234abcd",
    },
}

DUMMY_DELETE_ORDER_PAYLOAD = {
    "time": "2021-11-21T19:34:45.071+00:00",
    "status": "ok",
    "mode": "paper",
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
            activated_at=datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
            cancelled_at=datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
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
    _client=None,
    next="https://paper-trading.lemon.markets/v1/orders/?limit=10&page=3",
)

DUMMY_CREATE_ORDER_RESPONSE = CreateOrderResponse(
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
        estimated_price_total=66140000,
        notes="I want to attach a note to this order",
        idempotency="1234abcd",
        charge=20000,
        chargeable_at=datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
        key_creation_id="apk_pyJKKbbDDNympXsVwZzPp2nBVlTMTLRmxy",
    ),
)

DUMMY_ACTIVATE_ORDER_RESPONSE = ActivateOrderResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
)

DUMMY_ORDER_RESPONSE = GetOrderResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
    results=Order(
        id="ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
        isin="DE0008232125",
        isin_title="DEUTSCHE LUFTHANSA AG",
        expires_at=datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
        created_at=datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
        activated_at=datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
        cancelled_at=datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
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
        idempotency="1234abcd",
    ),
)

DUMMY_DELETE_ORDER_RESPONSE = DeleteOrderResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
)


class TestGetOrdersApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/orders", "method": "GET"}

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
            ({"status": ["inactive", "activated"]}, "status=inactive&status=activated"),
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
        httpserver.expect_oneshot_request(
            "/orders",
            query_string=query_string,
            method="GET",
        ).respond_with_json(DUMMY_ORDERS_PAYLOAD)
        DUMMY_ORDERS_RESPONSE._client = client.trading
        assert client.trading.orders.get(**function_kwargs) == DUMMY_ORDERS_RESPONSE

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/orders",
            method="GET",
        ).respond_with_json(DUMMY_ORDERS_PAYLOAD)
        DUMMY_ORDERS_RESPONSE._client = client.trading
        assert client.trading.orders.get() == DUMMY_ORDERS_RESPONSE


class TestCreateOrderApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.create(
            isin="DE0008232125",
            expires_at=7,
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
                "expires_at": "P7D",
                "side": "buy",
                "quantity": 1000,
                "venue": "xmun",
            },
        }

    @pytest.mark.parametrize(
        "expires_at,exp_expires_at",
        [("p7d", "P7D"), ("7d", "7D"), (7, "P7D"), (date(2021, 11, 7), "2021-11-07")],
    )
    def test_create_order(
        self, client: Api, httpserver: HTTPServer, expires_at, exp_expires_at
    ):
        httpserver.expect_oneshot_request(
            "/orders",
            method="POST",
            json={
                "isin": "DE0008232125",
                "expires_at": exp_expires_at,
                "side": "buy",
                "quantity": 1000,
                "venue": "xmun",
                "stop_price": 1000,
                "limit_price": 500,
                "notes": "foo",
                "idempotency": "bar",
            },
        ).respond_with_json(DUMMY_CREATE_ORDER_PAYLOAD)
        assert (
            client.trading.orders.create(
                isin="DE0008232125",
                expires_at=expires_at,
                side="buy",
                quantity=1000,
                venue="xmun",
                stop_price=1000,
                limit_price=500,
                notes="foo",
                idempotency="bar",
            )
            == DUMMY_CREATE_ORDER_RESPONSE
        )

    def test_fail_to_create_order_for_invalid_expires_at(self, client: Api):
        with pytest.raises(ValueError) as err:
            client.trading.orders.create(
                isin="DE0008232125",
                expires_at="invalid-expires-at-format",
                side="buy",
                quantity=1000,
                venue="xmun",
                stop_price=1000,
                limit_price=500,
                notes="foo",
                idempotency="bar",
            )

        assert (
            err.value.args[0]
            == "Invalid 'expires_at' format ('pXd' or 'Xd' are allowed where X is a non-negative integer)"
        )

    def test_create_order__no_expiration(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders",
            method="POST",
            json={
                "isin": "DE0008232125",
                "side": "buy",
                "quantity": 1000,
                "venue": "xmun",
                "stop_price": 1000,
                "limit_price": 500,
                "notes": "foo",
                "idempotency": "bar",
            },
        ).respond_with_json(DUMMY_CREATE_ORDER_PAYLOAD)
        assert (
            client.trading.orders.create(
                isin="DE0008232125",
                side="buy",
                quantity=1000,
                venue="xmun",
                stop_price=1000,
                limit_price=500,
                notes="foo",
                idempotency="bar",
            )
            == DUMMY_CREATE_ORDER_RESPONSE
        )


class TestActivateOrderApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.activate(order_id="DE0008232125")

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/orders/DE0008232125/activate",
            "method": "POST",
            "json": {},
        }

    def test_activate_order(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders/DE0008232125/activate",
            method="POST",
            json={"pin": "1234"},
        ).respond_with_json(DUMMY_ACTIVATE_ORDER_PAYLOAD)
        assert (
            client.trading.orders.activate(order_id="DE0008232125", pin="1234")
            == DUMMY_ACTIVATE_ORDER_RESPONSE
        )

    def test_raise_on_invalid_input(self, client: Api):
        with pytest.raises(ValueError):
            client.trading.orders.activate("")


class TestGetOrderApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.get_order(order_id="DE0008232125")

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/orders/DE0008232125",
            "method": "GET",
        }

    def test_get_order(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders/DE0008232125",
            method="GET",
        ).respond_with_json(DUMMY_ORDER_PAYLOAD)
        assert (
            client.trading.orders.get_order(order_id="DE0008232125")
            == DUMMY_ORDER_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders/DE0008232125",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/orders/DE0008232125",
            method="GET",
        ).respond_with_json(DUMMY_ORDER_PAYLOAD)

        assert (
            client.trading.orders.get_order(order_id="DE0008232125")
            == DUMMY_ORDER_RESPONSE
        )

    def test_raise_on_invalid_input(self, client: Api):
        with pytest.raises(ValueError):
            client.trading.orders.get_order("")


class TestDeleteOrderApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.orders.cancel(order_id="DE0008232125")

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/orders/DE0008232125",
            "method": "DELETE",
        }

    def test_delete_order(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders/DE0008232125",
            method="DELETE",
        ).respond_with_json(DUMMY_DELETE_ORDER_PAYLOAD)
        assert (
            client.trading.orders.cancel(order_id="DE0008232125")
            == DUMMY_DELETE_ORDER_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/orders/DE0008232125",
            method="DELETE",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/orders/DE0008232125",
            method="DELETE",
        ).respond_with_json(DUMMY_DELETE_ORDER_PAYLOAD)

        assert (
            client.trading.orders.cancel(order_id="DE0008232125")
            == DUMMY_DELETE_ORDER_RESPONSE
        )

    def test_raise_on_invalid_input(self, client: Api):
        with pytest.raises(ValueError):
            client.trading.orders.cancel("")
