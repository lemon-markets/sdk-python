MARKET_DATA_API_URL = "https://data.lemon.markets/v1/"


class Config:
    def __init__(self, api_token: str, market_data_api_url: str):
        self.api_token = api_token
        self.market_data_api_url = market_data_api_url
