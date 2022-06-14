from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from typing_extensions import Literal

from lemon.types import BaseModel, Environment

OrderSide = Literal["sell", "buy"]
OrderStatus = Literal[
    "inactive",
    "activated",
    "open",
    "in_progress",
    "canceling",
    "executed",
    "canceled",
    "expired",
    "rejected",
]
OrderType = Literal["market", "stop", "limit", "stop_limit"]
Venue = Literal["xmun", "allday"]


@dataclass
class RegulatoryInformation(BaseModel):
    costs_entry: Optional[int]
    costs_entry_pct: Optional[str]
    costs_running: int
    costs_running_pct: Optional[str]
    costs_product: int
    costs_product_pct: Optional[str]
    costs_exit: int
    costs_exit_pct: Optional[str]
    yield_reduction_year: Optional[int]
    yield_reduction_year_pct: Optional[str]
    yield_reduction_year_following: Optional[int]
    yield_reduction_year_following_pct: Optional[str]
    yield_reduction_year_exit: int
    yield_reduction_year_exit_pct: str
    estimated_holding_duration_years: Optional[str]
    estimated_yield_reduction_total: Optional[int]
    estimated_yield_reduction_total_pct: Optional[str]
    KIID: Optional[str]
    legal_disclaimer: str


@dataclass
class Order(BaseModel):
    id: str
    isin: str
    isin_title: str
    expires_at: datetime
    created_at: datetime
    side: OrderSide
    quantity: int
    stop_price: Optional[int]
    limit_price: Optional[int]
    estimated_price: Optional[int]
    estimated_price_total: Optional[int]
    venue: str
    status: OrderStatus
    type: OrderType
    executed_quantity: int
    executed_price: int
    executed_price_total: Optional[int]
    activated_at: Optional[datetime]
    executed_at: Optional[datetime]
    rejected_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    notes: Optional[str]
    charge: Optional[int]
    chargeable_at: Optional[datetime]
    key_creation_id: Optional[str]
    key_activation_id: Optional[str]
    regulatory_information: Optional[RegulatoryInformation]
    idempotency: Optional[str]


@dataclass
class GetOrdersResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Order]
    total: int
    page: int
    pages: int


@dataclass
class CreatedOrder(BaseModel):
    id: str
    status: OrderStatus
    created_at: datetime
    regulatory_information: RegulatoryInformation
    isin: str
    expires_at: datetime
    side: OrderSide
    quantity: int
    stop_price: Optional[int]
    limit_price: Optional[int]
    venue: Optional[str]
    estimated_price: int
    estimated_price_total: int
    notes: Optional[str]
    charge: Optional[int]
    chargeable_at: Optional[datetime]
    key_creation_id: Optional[str]
    idempotency: Optional[str]


@dataclass
class CreateOrderResponse(BaseModel):
    time: datetime
    mode: Environment
    results: CreatedOrder


@dataclass
class ActivateOrderResponse(BaseModel):
    time: datetime
    mode: Environment


@dataclass
class GetOrderResponse(BaseModel):
    time: datetime
    mode: Environment
    results: Order


@dataclass
class DeleteOrderResponse(BaseModel):
    time: datetime
    mode: Environment
