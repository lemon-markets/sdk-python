from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional

from lemon.helpers import Environment

StatementType = Literal["order_buy", "order_sell", "split", "import", "snx"]


@dataclass
class Position:
    isin: str
    isin_title: str
    quantity: int
    buy_price_avg: int
    estimated_price_total: int
    estimated_price: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Position":
        return Position(
            isin=data["isin"],
            isin_title=data["isin_title"],
            quantity=int(data["quantity"]),
            buy_price_avg=int(data["buy_price_avg"]),
            estimated_price_total=int(data["estimated_price_total"]),
            estimated_price=int(data["estimated_price"]),
        )


@dataclass
class GetPositionsResponse:
    time: datetime
    mode: Environment
    results: List[Position]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetPositionsResponse":
        return GetPositionsResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[Position._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )


@dataclass
class Statement:
    id: str
    order_id: str
    external_id: Optional[str]
    type: StatementType
    quantity: int
    isin: str
    isin_title: str
    date: date
    created_at: datetime

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Statement":
        return Statement(
            id=data["id"],
            order_id=data["order_id"],
            external_id=data["external_id"],
            type=data["type"],
            quantity=int(data["quantity"]),
            isin=data["isin"],
            isin_title=data["isin_title"],
            date=datetime.fromisoformat(data["date"]).date(),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class GetStatementsResponse:
    time: datetime
    mode: Environment
    results: List[Statement]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetStatementsResponse":
        return GetStatementsResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[Statement._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )


@dataclass
class Performance:
    isin: str
    isin_title: str
    profit: int
    loss: int
    quantity_bought: int
    quantity_sold: int
    quantity_open: int
    opened_at: datetime
    closed_at: datetime
    fees: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Performance":
        return Performance(
            isin=data["isin"],
            isin_title=data["isin_title"],
            profit=int(data["profit"]),
            loss=int(data["loss"]),
            quantity_bought=int(data["quantity_bought"]),
            quantity_sold=int(data["quantity_sold"]),
            quantity_open=int(data["quantity_open"]),
            opened_at=datetime.fromisoformat(data["opened_at"]),
            closed_at=datetime.fromisoformat(data["closed_at"]),
            fees=int(data["fees"]),
        )


@dataclass
class GetPerformanceResponse:
    time: datetime
    mode: Environment
    results: List[Performance]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetPerformanceResponse":
        return GetPerformanceResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[Performance._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )