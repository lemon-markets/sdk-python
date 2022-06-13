from datetime import date, datetime

from lemon.trading.model import (
    GetPerformanceResponse,
    GetPositionsResponse,
    GetStatementsResponse,
    Performance,
    Position,
    Statement,
)

GET_POSITIONS_RESPONSE = GetPositionsResponse(
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

DICT_GET_POSITIONS_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
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
    "total": 33,
    "page": 2,
    "pages": 4,
}

GET_STATEMENTS_RESPONSE = GetStatementsResponse(
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

DICT_GET_STATEMENTS_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
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
            "date": date(year=2021, month=12, day=10),
            "created_at": datetime.fromisoformat("2021-12-10T07:57:12.628+00:00"),
        },
    ],
    "total": 33,
    "page": 2,
    "pages": 4,
}

GET_PERFORMANCE_RESPONSE = GetPerformanceResponse(
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

DICT_GET_PERFORMANCE_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-21T19:34:45.071+00:00"),
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
            "opened_at": datetime.fromisoformat("2022-02-02T16:20:30.618+00:00"),
            "closed_at": datetime.fromisoformat("2022-02-03T12:32:00.762+00:00"),
            "fees": 40000,
        },
    ],
    "total": 37,
    "page": 2,
    "pages": 4,
}


def test_get_positions_response_is_serializable():
    assert GET_POSITIONS_RESPONSE.dict() == DICT_GET_POSITIONS_RESPONSE
    assert GET_POSITIONS_RESPONSE.json()


def test_get_statements_response_is_serializable():
    assert GET_STATEMENTS_RESPONSE.dict() == DICT_GET_STATEMENTS_RESPONSE
    assert GET_STATEMENTS_RESPONSE.json()


def test_get_performance_response_is_serializable():
    assert GET_PERFORMANCE_RESPONSE.dict() == DICT_GET_PERFORMANCE_RESPONSE
    assert GET_PERFORMANCE_RESPONSE.json()
