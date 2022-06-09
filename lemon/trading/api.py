from typing import Any, Dict, Optional

import requests

from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.trading.account.api import Account
from lemon.trading.orders.api import Orders
from lemon.trading.positions.api import Positions
from lemon.trading.user.api import User


class TradingApi:
    def __init__(self, config: Config):
        self._client = ApiClient(config.trading_api_url, config)

    @property
    def account(self) -> Account:
        return Account(self._client)

    @property
    def orders(self) -> Orders:
        return Orders(self._client)

    @property
    def positions(self) -> Positions:
        return Positions(self._client)

    @property
    def user(self) -> User:
        return User(self._client)

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
