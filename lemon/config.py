MARKET_DATA_API_URL = "https://data.lemon.markets/v1/"
LIVE_TRADING_API_URL = "https://trading.lemon.markets/v1/"
PAPER_TRADING_API_URL = "https://paper-trading.lemon.markets/v1/"


class Config:
    def __init__(
        self,
        api_token: str,
        market_data_api_url: str,
        trading_api_url: str,
        timeout: float,
        retry_count: int,
        retry_backoff_factor: float,
    ):
        self.api_token = api_token
        self.market_data_api_url = market_data_api_url
        self.trading_api_url = trading_api_url
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_backoff_factor = retry_backoff_factor
