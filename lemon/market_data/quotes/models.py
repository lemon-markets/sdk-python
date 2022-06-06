from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, TypeVar

T = TypeVar("T", int, float)
K = TypeVar("K", int, datetime)


@dataclass
class Quote(Generic[T, K]):
    isin: str
    b_v: T
    a_v: T
    b: T
    a: T
    t: K
    mic: str

    @staticmethod
    def _from_data(
        data: Dict[str, Any], t_type: Callable[[Any], T], k_type: Callable[[Any], K]
    ) -> "Quote[T, K]":
        return Quote(
            isin=data["isin"],
            b_v=t_type(data["b_v"]),
            a_v=t_type(data["a_v"]),
            b=t_type(data["b"]),
            a=t_type(data["a"]),
            t=k_type(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetQuotesResponse(Generic[T, K]):
    time: datetime
    results: List[Quote[T, K]]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(
        data: Dict[str, Any], t_type: Callable[[Any], T], k_type: Callable[[Any], K]
    ) -> "GetQuotesResponse[T, K]":
        return GetQuotesResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[
                Quote._from_data(entry, t_type, k_type) for entry in data["results"]
            ],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
