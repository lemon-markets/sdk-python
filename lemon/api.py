from typing import Optional

from lemon.config import MARKET_DATA_API_URL, Config
from lemon.market_data.api import MarketDataApi


class Api:
    def __init__(self, config: Config):
        self._config = config

    @property
    def market_data(self) -> MarketDataApi:
        return MarketDataApi(self._config)


def create(api_token: str, market_data_api_url: Optional[str] = None) -> Api:
    market_data_api_url = market_data_api_url or MARKET_DATA_API_URL
    return Api(Config(api_token=api_token, market_data_api_url=market_data_api_url))
