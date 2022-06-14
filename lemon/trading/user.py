from lemon.base import Client
from lemon.trading.model import GetUserResponse


class User:
    def __init__(self, client: Client):
        self._client = client

    def get(self) -> GetUserResponse:
        resp = self._client.get("user")
        return GetUserResponse._from_data(resp.json())
