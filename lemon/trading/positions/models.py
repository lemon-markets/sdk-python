from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from lemon.helpers import Environment


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
