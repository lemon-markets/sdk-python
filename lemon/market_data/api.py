from typing import Any, Dict, Optional

import requests

from lemon.config import Config
from lemon.helpers import ApiClient
from lemon.market_data.instruments import Instruments
from lemon.market_data.ohlc import Ohlc
from lemon.market_data.quotes import Quotes
from lemon.market_data.trades import Trades
from lemon.market_data.venues import Venues


class MarketDataApi:
    def __init__(self, config: Config):
        self._client = ApiClient(config.market_data_api_url, config)
        self._venues: Optional[Venues] = None
        self._instruments: Optional[Instruments] = None
        self._trades: Optional[Trades] = None
        self._quotes: Optional[Quotes] = None
        self._ohlc: Optional[Ohlc] = None

    @property
    def venues(self) -> Venues:
        if self._venues is None:
            self._venues = Venues(self._client)
        return self._venues

    @property
    def instruments(self) -> Instruments:
        if self._instruments is None:
            self._instruments = Instruments(self._client)
        return self._instruments

    @property
    def trades(self) -> Trades:
        if self._trades is None:
            self._trades = Trades(self._client)
        return self._trades

    @property
    def quotes(self) -> Quotes:
        if self._quotes is None:
            self._quotes = Quotes(self._client)
        return self._quotes

    @property
    def ohlc(self) -> Ohlc:
        if self._ohlc is None:
            self._ohlc = Ohlc(self._client)
        return self._ohlc

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
