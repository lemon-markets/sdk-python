from lemon.helpers import ApiClient
from lemon.trading.user.models import GetUserResponse


class User:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetUserResponse:
        resp = self._client.get("/v1/user")
        return GetUserResponse._from_data(resp.json())
