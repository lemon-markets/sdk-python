from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class OhlcData:
    isin: str
    o: float
    h: float
    l: float
    c: float
    v: float
    pbv: float
    t: datetime
    mic: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "OhlcData":
        return OhlcData(
            isin=data["isin"],
            o=data["o"],
            h=data["h"],
            l=data["l"],
            c=data["c"],
            v=data["v"],
            pbv=data["pbv"],
            t=datetime.fromisoformat(data["t"]),
            mic=data["mic"],
        )


@dataclass
class GetOhlcResponse:
    time: datetime
    results: List[OhlcData]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetOhlcResponse":
        return GetOhlcResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[OhlcData._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
