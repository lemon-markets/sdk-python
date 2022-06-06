from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, TypeVar

T = TypeVar("T", int, float)
K = TypeVar("K", int, datetime)


@dataclass
class Trade(Generic[T, K]):
    isin: str
    p: T
    v: T
    t: K
    mic: str

    @staticmethod
    def _from_data(
        data: Dict[str, Any], t_type: Callable[[Any], T], k_type: Callable[[Any], K]
    ) -> "Trade[T, K]":
        return Trade(
            isin=data["isin"],
            p=t_type(data["p"]),
            v=t_type(data["v"]),
            t=k_type(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetTradesResponse(Generic[T, K]):
    time: datetime
    results: List[Trade[T, K]]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(
        data: Dict[str, Any], t_type: Callable[[Any], T], k_type: Callable[[Any], K]
    ) -> "GetTradesResponse[T, K]":
        return GetTradesResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[
                Trade._from_data(entry, t_type, k_type) for entry in data["results"]
            ],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
