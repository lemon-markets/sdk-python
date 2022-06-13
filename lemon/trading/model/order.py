from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from lemon.helpers import BaseModel, Environment, as_or_none

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

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "RegulatoryInformation":
        return RegulatoryInformation(
            costs_entry=as_or_none(int, data.get("costs_entry")),
            costs_entry_pct=data.get("costs_entry_pct"),
            costs_running=int(data["costs_running"]),
            costs_running_pct=data.get("costs_running_pct"),
            costs_product=int(data["costs_product"]),
            costs_product_pct=data.get("costs_product_pct"),
            costs_exit=int(data["costs_exit"]),
            costs_exit_pct=data.get("costs_exit_pct"),
            yield_reduction_year=as_or_none(int, data.get("yield_reduction_year")),
            yield_reduction_year_pct=data.get("yield_reduction_year_pct"),
            yield_reduction_year_following=as_or_none(
                int, data.get("yield_reduction_year_following")
            ),
            yield_reduction_year_following_pct=data.get(
                "yield_reduction_year_following_pct"
            ),
            yield_reduction_year_exit=int(data["yield_reduction_year_exit"]),
            yield_reduction_year_exit_pct=data["yield_reduction_year_exit_pct"],
            estimated_holding_duration_years=data.get(
                "estimated_holding_duration_years"
            ),
            estimated_yield_reduction_total=as_or_none(
                int, data.get("estimated_yield_reduction_total")
            ),
            estimated_yield_reduction_total_pct=data.get(
                "estimated_yield_reduction_total_pct"
            ),
            KIID=data.get("KIID"),
            legal_disclaimer=data["legal_disclaimer"],
        )


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

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Order":
        print(data)
        return Order(
            id=data["id"],
            isin=data["isin"],
            isin_title=data["isin_title"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            side=data["side"],
            quantity=int(data["quantity"]),
            stop_price=as_or_none(int, data.get("stop_price")),
            limit_price=as_or_none(int, data.get("limit_price")),
            estimated_price=as_or_none(int, data.get("estimated_price")),
            estimated_price_total=as_or_none(int, data.get("estimated_price_total")),
            venue=data["venue"],
            status=data["status"],
            type=data["type"],
            executed_quantity=int(data["executed_quantity"]),
            executed_price=int(data["executed_price"]),
            executed_price_total=as_or_none(int, data.get("executed_price_total")),
            activated_at=as_or_none(datetime.fromisoformat, data.get("activated_at")),
            executed_at=as_or_none(datetime.fromisoformat, data.get("executed_at")),
            rejected_at=as_or_none(datetime.fromisoformat, data.get("rejected_at")),
            cancelled_at=as_or_none(datetime.fromisoformat, data.get("cancelled_at")),
            notes=data.get("notes"),
            charge=as_or_none(int, data.get("charge")),
            chargeable_at=as_or_none(datetime.fromisoformat, data.get("chargeable_at")),
            key_creation_id=data.get("key_creation_id"),
            key_activation_id=data.get("key_activation_id"),
            regulatory_information=as_or_none(
                RegulatoryInformation._from_data, data.get("regulatory_information")
            ),
            idempotency=data.get("idempotency"),
        )


@dataclass
class GetOrdersResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Order]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetOrdersResponse":
        return GetOrdersResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[Order._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )


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

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "CreatedOrder":
        return CreatedOrder(
            id=data["id"],
            status=data["status"],
            created_at=datetime.fromisoformat(data["created_at"]),
            regulatory_information=RegulatoryInformation._from_data(
                data["regulatory_information"]
            ),
            isin=data["isin"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            side=data["side"],
            quantity=int(data["quantity"]),
            stop_price=as_or_none(int, data.get("stop_price")),
            limit_price=as_or_none(int, data.get("limit_price")),
            venue=data.get("venue"),
            estimated_price=int(data["estimated_price"]),
            estimated_price_total=int(data["estimated_price_total"]),
            notes=data.get("notes"),
            charge=as_or_none(int, data.get("charge")),
            chargeable_at=as_or_none(datetime.fromisoformat, data.get("chargeable_at")),
            key_creation_id=data.get("key_creation_id"),
            idempotency=data.get("idempotency"),
        )


@dataclass
class CreateOrderResponse(BaseModel):
    time: datetime
    mode: Environment
    results: CreatedOrder

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "CreateOrderResponse":
        return CreateOrderResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=CreatedOrder._from_data(data["results"]),
        )


@dataclass
class ActivateOrderResponse(BaseModel):
    time: datetime
    mode: Environment

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "ActivateOrderResponse":
        return ActivateOrderResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
        )


@dataclass
class GetOrderResponse(BaseModel):
    time: datetime
    mode: Environment
    results: Order

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetOrderResponse":
        return GetOrderResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=Order._from_data(data["results"]),
        )


@dataclass
class DeleteOrderResponse(BaseModel):
    time: datetime
    mode: Environment

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "DeleteOrderResponse":
        return DeleteOrderResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
        )
