from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Quote:
    isin: str
    b_v: float
    a_v: float
    b: float
    a: float
    t: datetime
    mic: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Quote":
        return Quote(
            isin=data["isin"],
            b_v=data["b_v"],
            a_v=data["a_v"],
            b=data["b"],
            a=data["a"],
            t=datetime.fromisoformat(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetQuotesResponse:
    time: datetime
    results: List[Quote]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetQuotesResponse":
        return GetQuotesResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[Quote._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
