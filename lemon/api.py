import warnings

from typing_extensions import Literal

from lemon.market_data.api import MarketDataAPI
from lemon.streaming.api import StreamingAPI
from lemon.trading.api import TradingAPI

MARKET_DATA_API_URL = "https://data.lemon.markets/v1/"
LIVE_TRADING_API_URL = "https://trading.lemon.markets/v1/"
PAPER_TRADING_API_URL = "https://paper-trading.lemon.markets/v1/"
STREAMING_API_URL = "https://realtime.lemon.markets/v1/"


class Api:
    def __init__(
        self,
        market_data_api_token: str,
        trading_api_token: str,
        market_data_api_url: str,
        trading_api_url: str,
        streaming_api_url: str,
        timeout: float,
        retry_count: int,
        retry_backoff_factor: float,
    ):
        self._market_data = MarketDataAPI(
            api_token=market_data_api_token,
            market_data_api_url=market_data_api_url,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )
        self._trading = TradingAPI(
            api_token=trading_api_token,
            trading_api_url=trading_api_url,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )
        self._streaming = StreamingAPI(
            api_token=market_data_api_token,
            streaming_api_url=streaming_api_url,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )

    @property
    def market_data(self) -> MarketDataAPI:
        return self._market_data

    @property
    def trading(self) -> TradingAPI:
        return self._trading

    @property
    def streaming(self) -> StreamingAPI:
        return self._streaming


def create(
    market_data_api_token: str,
    trading_api_token: str,
    env: Literal["paper", "money", "live"] = "paper",
    timeout: float = 5,
    retry_count: int = 3,
    retry_backoff_factor: float = 0.1,
) -> Api:
    if env == "money":
        warnings.warn(
            "Usage of 'money' as env is deprecated, please use 'live' in the future",
            category=FutureWarning,
        )
    return Api(
        market_data_api_token=market_data_api_token,
        trading_api_token=trading_api_token,
        market_data_api_url=MARKET_DATA_API_URL,
        streaming_api_url=STREAMING_API_URL,
        trading_api_url=LIVE_TRADING_API_URL
        if env in ["money", "live"]
        else PAPER_TRADING_API_URL,
        timeout=timeout,
        retry_count=retry_count,
        retry_backoff_factor=retry_backoff_factor,
    )
