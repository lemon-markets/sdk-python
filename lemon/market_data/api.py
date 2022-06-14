from typing import Optional

from lemon.base import Client
from lemon.market_data.instruments import Instruments
from lemon.market_data.ohlc import Ohlc
from lemon.market_data.quotes import Quotes
from lemon.market_data.trades import Trades
from lemon.market_data.venues import Venues


class MarketDataAPI(Client):
    def __init__(
        self,
        api_token: str,
        market_data_api_url: str,
        timeout: float,
        retry_count: int,
        retry_backoff_factor: float,
    ):
        super().__init__(
            base_url=market_data_api_url,
            api_token=api_token,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )
        self._venues: Optional[Venues] = None
        self._instruments: Optional[Instruments] = None
        self._trades: Optional[Trades] = None
        self._quotes: Optional[Quotes] = None
        self._ohlc: Optional[Ohlc] = None

    @property
    def venues(self) -> Venues:
        if self._venues is None:
            self._venues = Venues(self)
        return self._venues

    @property
    def instruments(self) -> Instruments:
        if self._instruments is None:
            self._instruments = Instruments(self)
        return self._instruments

    @property
    def trades(self) -> Trades:
        if self._trades is None:
            self._trades = Trades(self)
        return self._trades

    @property
    def quotes(self) -> Quotes:
        if self._quotes is None:
            self._quotes = Quotes(self)
        return self._quotes

    @property
    def ohlc(self) -> Ohlc:
        if self._ohlc is None:
            self._ohlc = Ohlc(self)
        return self._ohlc
