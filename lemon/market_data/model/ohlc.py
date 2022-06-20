from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Union

from lemon.types import BaseModel


@dataclass
class OhlcData(BaseModel):
    isin: str
    o: Union[int, float]
    h: Union[int, float]
    l: Union[int, float]
    c: Union[int, float]
    v: int
    pbv: Union[int, float]
    t: Union[datetime, int]
    mic: str

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "OhlcData":
        return OhlcData(
            isin=data["isin"],
            o=t_type(data["o"]),
            h=t_type(data["h"]),
            l=t_type(data["l"]),
            c=t_type(data["c"]),
            v=int(data["v"]),
            pbv=t_type(data["pbv"]),
            t=k_type(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetOhlcResponse(BaseModel):
    time: datetime
    results: List[OhlcData]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "GetOhlcResponse":
        return GetOhlcResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[
                OhlcData._from_data(entry, t_type, k_type) for entry in data["results"]
            ],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
