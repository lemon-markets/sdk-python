from typing import Any, Dict, Optional

import requests

from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.trading.account import Account
from lemon.trading.orders import Orders
from lemon.trading.positions import Positions
from lemon.trading.user import User


class TradingApi:
    def __init__(self, config: Config):
        self._client = ApiClient(config.trading_api_url, config)
        self._account: Optional[Account] = None
        self._orders: Optional[Orders] = None
        self._positions: Optional[Positions] = None
        self._user: Optional[User] = None

    @property
    def account(self) -> Account:
        if self._account is None:
            self._account = Account(self._client)
        return self._account

    @property
    def orders(self) -> Orders:
        if self._orders is None:
            self._orders = Orders(self._client)
        return self._orders

    @property
    def positions(self) -> Positions:
        if self._positions is None:
            self._positions = Positions(self._client)
        return self._positions

    @property
    def user(self) -> User:
        if self._user is None:
            self._user = User(self._client)
        return self._user

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.get(url=url, params=params, headers=headers)

    def put(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.put(url=url, json=json, params=params, headers=headers)

    def post(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.post(url=url, json=json, params=params, headers=headers)

    def delete(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.delete(url=url, params=params, headers=headers)
