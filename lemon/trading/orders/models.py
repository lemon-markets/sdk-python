from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from lemon.helpers import Environment

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
]
OrderType = Literal["market", "stop", "limit", "stop_limit"]


@dataclass
class RegulatoryInformation:
    costs_entry: int
    costs_entry_pct: str
    costs_running: int
    costs_running_pct: str
    costs_product: int
    costs_product_pct: str
    costs_exit: int
    costs_exit_pct: str
    yield_reduction_year: int
    yield_reduction_year_pct: str
    yield_reduction_year_following: int
    yield_reduction_year_following_pct: str
    yield_reduction_year_exit: int
    yield_reduction_year_exit_pct: str
    estimated_holding_duration_years: str
    estimated_yield_reduction_total: int
    estimated_yield_reduction_total_pct: str
    KIID: str
    legal_disclaimer: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "RegulatoryInformation":
        return RegulatoryInformation(
            costs_entry=int(data["costs_entry"]),
            costs_entry_pct=data["costs_entry_pct"],
            costs_running=int(data["costs_running"]),
            costs_running_pct=data["costs_running_pct"],
            costs_product=int(data["costs_product"]),
            costs_product_pct=data["costs_product_pct"],
            costs_exit=int(data["costs_exit"]),
            costs_exit_pct=data["costs_exit_pct"],
            yield_reduction_year=int(data["yield_reduction_year"]),
            yield_reduction_year_pct=data["yield_reduction_year_pct"],
            yield_reduction_year_following=int(data["yield_reduction_year_following"]),
            yield_reduction_year_following_pct=data[
                "yield_reduction_year_following_pct"
            ],
            yield_reduction_year_exit=int(data["yield_reduction_year_exit"]),
            yield_reduction_year_exit_pct=data["yield_reduction_year_exit_pct"],
            estimated_holding_duration_years=data["estimated_holding_duration_years"],
            estimated_yield_reduction_total=int(
                data["estimated_yield_reduction_total"]
            ),
            estimated_yield_reduction_total_pct=data[
                "estimated_yield_reduction_total_pct"
            ],
            KIID=data["KIID"],
            legal_disclaimer=data["legal_disclaimer"],
        )


@dataclass
class Order:
    id: str
    isin: str
    isin_title: str
    expires_at: datetime
    created_at: datetime
    side: OrderSide
    quantity: int
    stop_price: Optional[int]
    limit_price: Optional[int]
    estimated_price: int
    estimated_price_total: int
    venue: str
    status: OrderStatus
    type: OrderType
    executed_quantity: int
    executed_price: int
    executed_price_total: int
    executed_at: datetime
    rejected_at: Optional[datetime]
    notes: str
    charge: int
    chargeable_at: datetime
    key_creation_id: str
    key_activation_id: str
    regulatory_information: RegulatoryInformation
    idempotency: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Order":
        return Order(
            id=data["id"],
            isin=data["isin"],
            isin_title=data["isin_title"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            side=data["side"],
            quantity=int(data["quantity"]),
            stop_price=int(data["stop_price"])
            if data["stop_price"] is not None
            else None,
            limit_price=int(data["limit_price"])
            if data["limit_price"] is not None
            else None,
            estimated_price=int(data["estimated_price"]),
            estimated_price_total=int(data["estimated_price_total"]),
            venue=data["venue"],
            status=data["status"],
            type=data["type"],
            executed_quantity=int(data["executed_quantity"]),
            executed_price=int(data["executed_price"]),
            executed_price_total=int(data["executed_price_total"]),
            executed_at=datetime.fromisoformat(data["executed_at"]),
            rejected_at=datetime.fromisoformat(data["rejected_at"])
            if data["rejected_at"] is not None
            else None,
            notes=data["notes"],
            charge=int(data["charge"]),
            chargeable_at=datetime.fromisoformat(data["chargeable_at"]),
            key_creation_id=data["key_creation_id"],
            key_activation_id=data["key_activation_id"],
            regulatory_information=RegulatoryInformation._from_data(
                data["regulatory_information"]
            ),
            idempotency=data["idempotency"],
        )


@dataclass
class GetOrdersResponse:
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
class CreatedOrder:
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
    venue: str
    estimated_price: int
    notes: str
    idempotency: str
    charge: int
    chargeable_at: datetime
    key_creation_id: str

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
            stop_price=int(data["stop_price"])
            if data["stop_price"] is not None
            else None,
            limit_price=int(data["limit_price"])
            if data["limit_price"] is not None
            else None,
            venue=data["venue"],
            estimated_price=int(data["estimated_price"]),
            notes=data["notes"],
            idempotency=data["idempotency"],
            charge=int(data["charge"]),
            chargeable_at=datetime.fromisoformat(data["chargeable_at"]),
            key_creation_id=data["key_creation_id"],
        )


@dataclass
class CreateOrderResponse:
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
