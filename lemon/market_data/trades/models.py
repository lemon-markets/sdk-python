from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar("T", int, float)
K = TypeVar("K", int, datetime)


@dataclass
class Trade:
    isin: str
    p: Union[int, float]
    v: int
    t: Union[datetime, int]
    mic: str

    @staticmethod
    def _from_data(
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "Trade":
        return Trade(
            isin=data["isin"],
            p=t_type(data["p"]),
            v=data["v"],
            t=k_type(data["t"]),
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
    def _from_data(
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "GetTradesResponse":
        return GetTradesResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[
                Trade._from_data(entry, t_type, k_type) for entry in data["results"]
            ],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
