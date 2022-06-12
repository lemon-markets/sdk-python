from datetime import date
from typing import Optional, Union

from lemon.helpers import ApiClient, Days, handle_trading_errors
from lemon.trading.model import (
    ActivateOrderResponse,
    CreateOrderResponse,
    DeleteOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    OrderSide,
    OrderStatus,
    OrderType,
    Venue,
)


class Orders:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        from_: Optional[date] = None,
        to: Optional[date] = None,
        isin: Optional[str] = None,
        side: Optional[OrderSide] = None,
        status: Optional[OrderStatus] = None,
        type: Optional[OrderType] = None,
        key_creation_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetOrdersResponse:
        resp = self._client.get(
            "orders",
            params={
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
        if not resp.ok:
            handle_trading_errors(resp.json())
        return GetOrdersResponse._from_data(resp.json())

    def create(
        self,
        isin: str,
        side: OrderSide,
        quantity: int,
        expires_at: Union[date, Days, None] = None,
        stop_price: Optional[int] = None,
        limit_price: Optional[int] = None,
        venue: Optional[Venue] = None,
        notes: Optional[str] = None,
        idempotency: Optional[str] = None,
    ) -> CreateOrderResponse:
        if isinstance(expires_at, date):
            expires_at_str = expires_at.isoformat()
        elif isinstance(expires_at, int):
            expires_at_str = f"P{expires_at}D"
        else:
            expires_at_str = None

        resp = self._client.post(
            "orders",
            json={
                "isin": isin,
                "expires_at": expires_at_str,
                "side": side,
                "quantity": quantity,
                "venue": venue,
                "stop_price": stop_price,
                "limit_price": limit_price,
                "notes": notes,
                "idempotency": idempotency,
            },
        )
        if not resp.ok:
            handle_trading_errors(resp.json())
        return CreateOrderResponse._from_data(resp.json())

    def activate(
        self, order_id: str, pin: Optional[str] = None
    ) -> ActivateOrderResponse:
        resp = self._client.post(
            f"orders/{order_id}/activate",
            json={"pin": pin},
        )
        if not resp.ok:
            handle_trading_errors(resp.json())
        return ActivateOrderResponse._from_data(resp.json())

    def get_order(self, order_id: str) -> GetOrderResponse:
        resp = self._client.get(f"orders/{order_id}")
        if not resp.ok:
            handle_trading_errors(resp.json())
        return GetOrderResponse._from_data(resp.json())

    def delete(self, order_id: str) -> DeleteOrderResponse:
        resp = self._client.delete(f"orders/{order_id}")
        if not resp.ok:
            handle_trading_errors(resp.json())
        return DeleteOrderResponse._from_data(resp.json())
