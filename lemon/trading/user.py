from lemon.helpers import ApiClient
from lemon.trading.model import GetUserResponse


class User:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetUserResponse:
        resp = self._client.get("user")
        return GetUserResponse._from_data(resp.json())
