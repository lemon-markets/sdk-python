from lemon.helpers import ApiClient
from lemon.trading.account.models import GetAccountResponse


class Account:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetAccountResponse:
        resp = self._client.get("/account")
        return GetAccountResponse._from_data(resp.json())
