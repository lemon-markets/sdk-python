from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.trading.account.api import Account
from lemon.trading.orders.api import Orders


class TradingApi:
    def __init__(self, config: Config):
        self._config = config

    @property
    def account(self) -> Account:
        return Account(ApiClient(self._config.trading_api_url, self._config))

    @property
    def orders(self) -> Orders:
        return Orders(ApiClient(self._config.trading_api_url, self._config))
