from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from typing_extensions import Literal

from lemon.types import BaseModel


@dataclass
class InstrumentVenue(BaseModel):
    name: str
    title: str
    mic: str
    is_open: bool
    tradable: bool
    currency: str


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


@dataclass
class GetInstrumentsResponse(BaseModel):
    time: datetime
    results: List[Instrument]
    total: int
    page: int
    pages: int
