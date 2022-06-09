from functools import cached_property

from lemon.config import MARKET_DATA_API_URL, PAPER_TRADING_API_URL, Config
from lemon.market_data.api import MarketDataApi
from lemon.trading.api import TradingApi


class Api:
    def __init__(self, config: Config):
        self._config = config

    @cached_property
    def market_data(self) -> MarketDataApi:
        return MarketDataApi(self._config)

    @cached_property
    def trading(self) -> TradingApi:
        return TradingApi(self._config)


def create(
    api_token: str,
    market_data_api_url: str = MARKET_DATA_API_URL,
    trading_api_url: str = PAPER_TRADING_API_URL,
    timeout: int = 5,
    retry_count: int = 3,
    retry_backoff_factor: float = 0.1,
) -> Api:
    return Api(
        Config(
            api_token=api_token,
            market_data_api_url=market_data_api_url,
            trading_api_url=trading_api_url,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )
    )
