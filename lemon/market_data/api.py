from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.market_data.venues.api import Venues


class MarketDataApi:
    def __init__(self, config: Config):
        self._config = config

    @property
    def venues(self) -> Venues:
        return Venues(ApiClient(self._config.market_data_api_url, self._config))
