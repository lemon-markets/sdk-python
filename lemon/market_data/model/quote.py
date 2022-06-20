from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Union

from lemon.types import BaseModel


@dataclass
class Quote(BaseModel):
    isin: str
    b_v: int
    a_v: int
    b: Union[int, float]
    a: Union[int, float]
    t: Union[datetime, int]
    mic: str

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "Quote":
        return Quote(
            isin=data["isin"],
            b_v=int(data["b_v"]),
            a_v=int(data["a_v"]),
            b=t_type(data["b"]),
            a=t_type(data["a"]),
            t=k_type(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetQuotesResponse(BaseModel):
    time: datetime
    results: List[Quote]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
        data: Dict[str, Any],
        t_type: Callable[[Any], Union[int, float]],
        k_type: Callable[[Any], Union[datetime, int]],
    ) -> "GetQuotesResponse":
        return GetQuotesResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[
                Quote._from_data(entry, t_type, k_type) for entry in data["results"]
            ],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
