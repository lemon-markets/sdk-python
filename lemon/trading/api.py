from typing import Optional

from lemon.base import Client
from lemon.trading.account import Account
from lemon.trading.orders import Orders
from lemon.trading.positions import Positions
from lemon.trading.user import User


class TradingAPI(Client):
    def __init__(
        self,
        api_token: str,
        trading_api_url: str,
        timeout: float,
        retry_count: int,
        retry_backoff_factor: float,
    ):
        super().__init__(
            base_url=trading_api_url,
            api_token=api_token,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )
        self._account: Optional[Account] = None
        self._orders: Optional[Orders] = None
        self._positions: Optional[Positions] = None
        self._user: Optional[User] = None

    @property
    def account(self) -> Account:
        if self._account is None:
            self._account = Account(self)
        return self._account

    @property
    def orders(self) -> Orders:
        if self._orders is None:
            self._orders = Orders(self)
        return self._orders

    @property
    def positions(self) -> Positions:
        if self._positions is None:
            self._positions = Positions(self)
        return self._positions

    @property
    def user(self) -> User:
        if self._user is None:
            self._user = User(self)
        return self._user
