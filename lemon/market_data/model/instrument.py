from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from lemon.helpers import BaseModel


@dataclass
class InstrumentVenue(BaseModel):
    name: str
    title: str
    mic: str
    is_open: bool
    tradable: bool
    currency: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "InstrumentVenue":
        return InstrumentVenue(
            name=data["name"],
            title=data["title"],
            mic=data["mic"],
            is_open=data["is_open"],
            tradable=data["tradable"],
            currency=data["currency"],
        )


InstrumentType = Literal["stock", "bond", "warrant", "fund", "etf"]


@dataclass
class Instrument(BaseModel):
    isin: str
    wkn: str
    name: str
    title: Optional[str]
    symbol: Optional[str]
    type: InstrumentType
    venues: List[InstrumentVenue]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Instrument":
        return Instrument(
            isin=data["isin"],
            wkn=data["wkn"],
            name=data["name"],
            title=data.get("title"),
            symbol=data.get("symbol"),
            type=data["type"],
            venues=[InstrumentVenue._from_data(entry) for entry in data["venues"]],
        )


@dataclass
class GetInstrumentsResponse(BaseModel):
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
