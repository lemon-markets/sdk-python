from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Union

from lemon.types import BaseModel


@dataclass
class Trade(BaseModel):
    isin: str
    p: Union[int, float]
    pbv: Union[int, float]
    v: int
    t: Union[datetime, int]
    mic: str

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "Trade":
        return Trade(
            isin=data["isin"],
            p=t_type(data["p"]),
            pbv=t_type(data["pbv"]),
            v=int(data["v"]),
            t=k_type(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetTradesResponse(BaseModel):
    time: datetime
    results: List[Trade]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
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
