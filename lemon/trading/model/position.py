from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional

from lemon.helpers import Environment, SerializableMixin, as_or_none, to_date

StatementType = Literal["order_buy", "order_sell", "split", "import", "snx"]


@dataclass
class Position(SerializableMixin):
    isin: str
    isin_title: str
    quantity: int
    buy_price_avg: int
    estimated_price_total: Optional[int]
    estimated_price: Optional[int]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Position":
        return Position(
            isin=data["isin"],
            isin_title=data["isin_title"],
            quantity=int(data["quantity"]),
            buy_price_avg=int(data["buy_price_avg"]),
            estimated_price_total=as_or_none(int, data.get("estimated_price_total")),
            estimated_price=as_or_none(int, data.get("estimated_price")),
        )


@dataclass
class GetPositionsResponse(SerializableMixin):
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
class Statement(SerializableMixin):
    id: str
    order_id: Optional[str]
    external_id: Optional[str]
    type: StatementType
    quantity: int
    isin: str
    isin_title: Optional[str]
    date: date
    created_at: datetime

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Statement":
        return Statement(
            id=data["id"],
            order_id=data.get("order_id"),
            external_id=data.get("external_id"),
            type=data["type"],
            quantity=int(data["quantity"]),
            isin=data["isin"],
            isin_title=data.get("isin_title"),
            date=to_date(data["date"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class GetStatementsResponse(SerializableMixin):
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
class Performance(SerializableMixin):
    isin: str
    isin_title: str
    profit: int
    loss: int
    quantity_bought: int
    quantity_sold: int
    quantity_open: int
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]
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
            opened_at=as_or_none(datetime.fromisoformat, data.get("opened_at")),
            closed_at=as_or_none(datetime.fromisoformat, data.get("closed_at")),
            fees=int(data["fees"]),
        )


@dataclass
class GetPerformanceResponse(SerializableMixin):
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
