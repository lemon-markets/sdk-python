from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Venue:
    name: str
    title: str
    mic: str
    is_open: bool
    tradable: bool
    currency: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Venue":
        return Venue(
            name=data["name"],
            title=data["title"],
            mic=data["mic"],
            is_open=data["is_open"],
            tradable=data["tradable"],
            currency=data["currency"],
        )


@dataclass
class Instrument:
    isin: str
    wkn: str
    name: str
    title: str
    symbol: str
    type: str
    venues: List[Venue]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Instrument":
        return Instrument(
            isin=data["isin"],
            wkn=data["wkn"],
            name=data["name"],
            title=data["title"],
            symbol=data["symbol"],
            type=data["type"],
            venues=[Venue._from_data(entry) for entry in data["venues"]],
        )


@dataclass
class GetInstrumentsResponse:
    time: datetime
    results: List[Instrument]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetInstrumentsResponse":
        return GetInstrumentsResponse(
            time=datetime.fromisoformat(data["time"]),
            results=[Instrument._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
