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
        pool_connections: int,
        pool_maxsize: int,
    ):
        super().__init__(
            base_url=trading_api_url,
            api_token=api_token,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
        )
        self._account = Account(self)
        self._orders = Orders(self)
        self._positions = Positions(self)
        self._user = User(self)

    @property
    def account(self) -> Account:
        return self._account

    @property
    def orders(self) -> Orders:
        return self._orders

    @property
    def positions(self) -> Positions:
        return self._positions

    @property
    def user(self) -> User:
        return self._user
