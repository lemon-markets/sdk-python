from datetime import date, datetime
from typing import Optional

from lemon.helpers import ApiClient
from lemon.trading.orders.models import (
    ActivateOrderResponse,
    CreateOrderResponse,
    GetOrdersResponse,
    OrderSide,
    OrderStatus,
    OrderType,
)


class Orders:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        isin: Optional[str] = None,
        side: Optional[OrderSide] = None,
        status: Optional[OrderStatus] = None,
        type: Optional[OrderType] = None,
        key_creation_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetOrdersResponse:
        resp = self._client.get(
            "/orders",
            query_params={
                "from": from_,
                "to": to,
                "isin": isin,
                "side": side,
                "status": status,
                "type": type,
                "key_creation_id": key_creation_id,
                "limit": limit,
                "page": page,
            },
        )
        return GetOrdersResponse._from_data(resp.json())

    def create(
        self,
        isin: str,
        expires_at: date,
        side: OrderSide,
        quantity: int,
        venue: str,
        stop_price: Optional[int] = None,
        limit_price: Optional[int] = None,
        notes: Optional[str] = None,
        idempotency: Optional[str] = None,
    ) -> CreateOrderResponse:
        resp = self._client.post(
            "/orders",
            data={
                "isin": isin,
                "expires_at": expires_at.isoformat(),
                "side": side,
                "quantity": quantity,
                "venue": venue,
                "stop_price": stop_price,
                "limit_price": limit_price,
                "notes": notes,
                "idempotency": idempotency,
            },
        )
        return CreateOrderResponse._from_data(resp.json())

    def activate(self, order_id: str, pin: str) -> ActivateOrderResponse:
        resp = self._client.post(
            f"/orders/{order_id}/activate",
            data={"pin": pin},
        )
        return ActivateOrderResponse._from_data(resp.json())
