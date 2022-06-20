from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

from typing_extensions import Literal

from lemon.types import BaseModel, Environment

StatementType = Literal["order_buy", "order_sell", "split", "import", "snx"]


@dataclass
class Position(BaseModel):
    isin: str
    isin_title: str
    quantity: int
    buy_price_avg: int
    estimated_price_total: Optional[int]
    estimated_price: Optional[int]


@dataclass
class GetPositionsResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Position]
    total: int
    page: int
    pages: int


@dataclass
class Statement(BaseModel):
    id: str
    order_id: Optional[str]
    external_id: Optional[str]
    type: StatementType
    quantity: int
    isin: str
    isin_title: Optional[str]
    date: date
    created_at: datetime


@dataclass
class GetStatementsResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Statement]
    total: int
    page: int
    pages: int


@dataclass
class Performance(BaseModel):
    isin: str
    isin_title: str
    profit: int
    loss: int
    quantity_bought: int
    quantity_sold: int
    quantity_open: int
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]
    fees: int


@dataclass
class GetPerformanceResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Performance]
    total: int
    page: int
    pages: int
