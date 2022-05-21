from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Trade:
    isin: str
    p: float
    v: float
    t: datetime
    mic: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Trade":
        return Trade(
            isin=data["isin"],
            p=data["p"],
            v=data["v"],
            t=datetime.fromisoformat(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetTradesResponse:
    time: datetime
    results: List[Trade]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetTradesResponse":
        return GetTradesResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[Trade._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
