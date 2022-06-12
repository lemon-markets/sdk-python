from lemon.helpers import ApiClient, handle_trading_errors
from lemon.trading.model import GetUserResponse


class User:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetUserResponse:
        resp = self._client.get("user")
        if not resp.ok:
            handle_trading_errors(resp.json())
        return GetUserResponse._from_data(resp.json())
