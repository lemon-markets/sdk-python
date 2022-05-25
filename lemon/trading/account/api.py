from lemon.helpers import ApiClient
from lemon.trading.account.models import EditAccountPayload, GetAccountResponse


class Account:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetAccountResponse:
        resp = self._client.get("/account")
        return GetAccountResponse._from_data(resp.json())

    def update(self, data: EditAccountPayload) -> GetAccountResponse:
        resp = self._client.put("/account", data=data)
        return GetAccountResponse._from_data(resp.json())
