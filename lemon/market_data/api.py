from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.market_data.instruments.api import Instruments
from lemon.market_data.venues.api import Venues


class MarketDataApi:
    def __init__(self, config: Config):
        self._config = config

    @property
    def venues(self) -> Venues:
        return Venues(ApiClient(self._config.market_data_api_url, self._config))

    @property
    def instruments(self) -> Instruments:
        return Instruments(ApiClient(self._config.market_data_api_url, self._config))
