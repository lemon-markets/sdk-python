from lemon.config import Config
from lemon.market_data.api import MarketDataApi


class LemonApi:
    def __init__(self, config: Config):
        self._config = config

    @property
    def market_data(self) -> MarketDataApi:
        return MarketDataApi(self._config)
