from datetime import datetime

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

GET_ORDERS_RESPONSE = GetOrdersResponse(
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
    _headers=None,
    next=None,
)

DICT_GET_ORDERS_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    "mode": "paper",
    "results": [
        {
            "id": "ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
            "isin": "DE0008232125",
            "isin_title": "DEUTSCHE LUFTHANSA AG",
            "expires_at": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
            "created_at": datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
            "activated_at": datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
            "cancelled_at": datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
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
            "executed_at": datetime.fromisoformat("2021-11-04T12:25:12.402+00:00"),
            "rejected_at": None,
            "notes": "My Notes",
            "charge": 20000,
            "chargeable_at": datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
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
    "total": 33,
    "page": 2,
    "pages": 4,
    "_client": None,
    "_headers": None,
    "next": None,
}

CREATE_ORDER_RESPONSE = CreateOrderResponse(
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

DICT_CREATE_ORDER_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    "mode": "paper",
    "results": {
        "id": "ord_pyPGQggmmj0jhlLHw2nfM92Hm9PmgTYq9K",
        "created_at": datetime.fromisoformat("2021-11-15T13:58:19.981+00:00"),
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
        "expires_at": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
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
        "chargeable_at": datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
        "key_creation_id": "apk_pyJKKbbDDNympXsVwZzPp2nBVlTMTLRmxy",
    },
}

ACTIVATE_ORDER_RESPONSE = ActivateOrderResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
)

DICT_ACTIVATE_ORDER_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    "mode": "paper",
}


GET_ORDER_RESPONSE = GetOrderResponse(
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

DICT_GET_ORDER_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    "mode": "paper",
    "results": {
        "id": "ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
        "isin": "DE0008232125",
        "isin_title": "DEUTSCHE LUFTHANSA AG",
        "expires_at": datetime.fromisoformat("2021-11-07T22:59:00.000+00:00"),
        "created_at": datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
        "activated_at": datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
        "cancelled_at": datetime.fromisoformat("2021-11-04T12:25:30.063+00:00"),
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
        "executed_at": datetime.fromisoformat("2021-11-04T12:25:12.402+00:00"),
        "rejected_at": None,
        "notes": "My Notes",
        "charge": 20000,
        "chargeable_at": datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
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

DELETE_ORDER_RESPONSE = DeleteOrderResponse(
    time=datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    mode="paper",
)

DICT_DELETE_ORDER_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
    "mode": "paper",
}


def test_get_orders_response_is_serializable():
    assert GET_ORDERS_RESPONSE.dict() == DICT_GET_ORDERS_RESPONSE
    assert GET_ORDERS_RESPONSE.json()


def test_create_order_response_is_serializable():
    assert CREATE_ORDER_RESPONSE.dict() == DICT_CREATE_ORDER_RESPONSE
    assert CREATE_ORDER_RESPONSE.json()


def test_activate_order_response_is_serializable():
    assert ACTIVATE_ORDER_RESPONSE.dict() == DICT_ACTIVATE_ORDER_RESPONSE
    assert ACTIVATE_ORDER_RESPONSE.json()


def test_get_order_response_is_serializable():
    assert GET_ORDER_RESPONSE.dict() == DICT_GET_ORDER_RESPONSE
    assert GET_ORDER_RESPONSE.json()


def test_delete_order_response_is_serializable():
    assert DELETE_ORDER_RESPONSE.dict() == DICT_DELETE_ORDER_RESPONSE
    assert DELETE_ORDER_RESPONSE.json()
