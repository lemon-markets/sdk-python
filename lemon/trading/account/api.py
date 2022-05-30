from typing import Optional

from lemon.helpers import ApiClient, Sorting
from lemon.trading.account.models import (
    BankStatementType,
    EditAccountPayload,
    GetAccountResponse,
    GetBankStatementsResponse,
    GetWithdrawalsResponse,
    WithdrawResponse,
)


class Account:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetAccountResponse:
        resp = self._client.get("/account")
        return GetAccountResponse._from_data(resp.json())

    def update(self, data: EditAccountPayload) -> GetAccountResponse:
        resp = self._client.put("/account", data=data)
        return GetAccountResponse._from_data(resp.json())

    def get_withdrawals(
        self, limit: Optional[int] = None, page: Optional[int] = None
    ) -> GetWithdrawalsResponse:
        resp = self._client.get(
            "/account/withdrawals",
            query_params={
                "limit": limit,
                "page": page,
            },
        )
        return GetWithdrawalsResponse._from_data(resp.json())

    def withdraw(
        self,
        amount: int,
        pin: str,
        idempotency: Optional[str] = None,
    ) -> WithdrawResponse:
        resp = self._client.post(
            "/account/withdrawals",
            data={
                "amount": amount,
                "pin": pin,
                "idempotency": idempotency,
            },
        )
        return WithdrawResponse._from_data(resp.json())

    def get_bank_statements(
        self,
        type: Optional[BankStatementType] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetBankStatementsResponse:
        resp = self._client.get(
            "/account/bankstatements",
            query_params={
                "type": type,
                "from": from_,
                "to": to,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetBankStatementsResponse._from_data(resp.json())
