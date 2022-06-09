from typing import Any, Dict, Optional

import requests

from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.market_data.instruments.api import Instruments
from lemon.market_data.ohlc.api import Ohlc
from lemon.market_data.quotes.api import Quotes
from lemon.market_data.trades.api import Trades
from lemon.market_data.venues.api import Venues


class MarketDataApi:
    def __init__(self, config: Config):
        self._client = ApiClient(config.market_data_api_url, config)

    @property
    def venues(self) -> Venues:
        return Venues(self._client)

    @property
    def instruments(self) -> Instruments:
        return Instruments(self._client)

    @property
    def trades(self) -> Trades:
        return Trades(self._client)

    @property
    def quotes(self) -> Quotes:
        return Quotes(self._client)

    @property
    def ohlc(self) -> Ohlc:
        return Ohlc(self._client)

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.get(url=url, params=params, headers=headers)

    def put(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.put(url=url, json=json, params=params, headers=headers)

    def post(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.post(url=url, json=json, params=params, headers=headers)

    def delete(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        return self._client.delete(url=url, params=params, headers=headers)
