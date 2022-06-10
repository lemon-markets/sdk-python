from typing import Optional

from typing_extensions import Literal

from lemon.config import (
    LIVE_TRADING_API_URL,
    MARKET_DATA_API_URL,
    PAPER_TRADING_API_URL,
    Config,
)
from lemon.market_data.api import MarketDataApi
from lemon.trading.api import TradingApi


class Api:
    def __init__(self, config: Config):
        self._config = config
        self._market_data: Optional[MarketDataApi] = None
        self._trading: Optional[TradingApi] = None

    @property
    def market_data(self) -> MarketDataApi:
        if self._market_data is None:
            self._market_data = MarketDataApi(self._config)
        return self._market_data

    @property
    def trading(self) -> TradingApi:
        if self._trading is None:
            self._trading = TradingApi(self._config)
        return self._trading


def create(
    api_token: str,
    env: Literal["paper", "money"] = "paper",
    timeout: float = 5,
    retry_count: int = 3,
    retry_backoff_factor: float = 0.1,
) -> Api:
    return Api(
        Config(
            api_token=api_token,
            market_data_api_url=MARKET_DATA_API_URL,
            trading_api_url=LIVE_TRADING_API_URL
            if env == "money"
            else PAPER_TRADING_API_URL,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )
    )
