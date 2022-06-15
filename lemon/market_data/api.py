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
        self._venues = Venues(self)
        self._instruments = Instruments(self)
        self._trades = Trades(self)
        self._quotes = Quotes(self)
        self._ohlc = Ohlc(self)

    @property
    def venues(self) -> Venues:
        return self._venues

    @property
    def instruments(self) -> Instruments:
        return self._instruments

    @property
    def trades(self) -> Trades:
        return self._trades

    @property
    def quotes(self) -> Quotes:
        return self._quotes

    @property
    def ohlc(self) -> Ohlc:
        return self._ohlc
