from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, TypeVar

DayOffset = int

T = TypeVar("T", int, float)
K = TypeVar("K", int, datetime)


@dataclass
class OhlcData(Generic[T, K]):
    isin: str
    o: T
    h: T
    l: T
    c: T
    v: T
    pbv: T
    t: K
    mic: str

    @staticmethod
    def _from_data(
        data: Dict[str, Any], t_type: Callable[[Any], T], k_type: Callable[[Any], K]
    ) -> "OhlcData[T, K]":
        return OhlcData(
            isin=data["isin"],
            o=t_type(data["o"]),
            h=t_type(data["h"]),
            l=t_type(data["l"]),
            c=t_type(data["c"]),
            v=t_type(data["v"]),
            pbv=t_type(data["pbv"]),
            t=k_type(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetOhlcResponse(Generic[T, K]):
    time: datetime
    results: List[OhlcData[T, K]]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(
        data: Dict[str, Any], t_type: Callable[[Any], T], k_type: Callable[[Any], K]
    ) -> "GetOhlcResponse[T, K]":
        return GetOhlcResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[
                OhlcData._from_data(entry, t_type, k_type) for entry in data["results"]
            ],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
