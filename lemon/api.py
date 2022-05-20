from lemon.config import Config
from lemon.market_data.api import MarketDataApi


class LemonApi:
    def __init__(self, config: Config):
        self._config = config

    @property
    def market_data(self) -> MarketDataApi:
        return MarketDataApi(self._config)


def create(api_token: str, api_url: str) -> LemonApi:
    return LemonApi(Config(api_token=api_token, api_url=api_url))
