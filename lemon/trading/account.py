from datetime import date
from typing import Optional, Union

from typing_extensions import Literal

from lemon.base import Client
from lemon.trading.model import (
    BankStatementType,
    GetAccountResponse,
    GetBankStatementsResponse,
    GetDocumentResponse,
    GetDocumentsResponse,
    GetWithdrawalsResponse,
    WithdrawResponse,
)
from lemon.types import Sorting


class Account:
    def __init__(self, client: Client):
        self._client = client

    def get(self) -> GetAccountResponse:
        resp = self._client.get("account")
        return GetAccountResponse._from_data(resp.json())

    def update(
        self,
        address_street: Optional[str] = None,
        address_street_number: Optional[str] = None,
        address_city: Optional[str] = None,
        address_postal_code: Optional[str] = None,
        address_country: Optional[str] = None,
    ) -> GetAccountResponse:
        resp = self._client.put(
            "account",
            json={
                "address_street": address_street,
                "address_street_number": address_street_number,
                "address_city": address_city,
                "address_postal_code": address_postal_code,
                "address_country": address_country,
            },
        )
        return GetAccountResponse._from_data(resp.json())

    def get_withdrawals(
        self, limit: Optional[int] = None, page: Optional[int] = None
    ) -> GetWithdrawalsResponse:
        resp = self._client.get(
            "account/withdrawals",
            params={
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
            "account/withdrawals",
            json={
                "amount": amount,
                "pin": pin,
                "idempotency": idempotency,
            },
        )
        return WithdrawResponse._from_data(resp.json())

    def get_bank_statements(
        self,
        type: Optional[BankStatementType] = None,
        from_: Union[date, Literal["beginning"], None] = None,
        to: Optional[date] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetBankStatementsResponse:
        resp = self._client.get(
            "account/bankstatements",
            params={
                "type": type,
                "from": from_,
                "to": to,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetBankStatementsResponse._from_data(resp.json())

    def get_documents(
        self,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetDocumentsResponse:
        resp = self._client.get(
            "account/documents",
            params={
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetDocumentsResponse._from_data(resp.json())

    def get_document(
        self, document_id: str, no_redirect: Optional[bool] = None
    ) -> GetDocumentResponse:
        document_id = document_id.strip()
        if not document_id:
            raise ValueError("document_id is empty string")

        resp = self._client.get(
            f"account/documents/{document_id}", params={"no_redirect": no_redirect}
        )
        return GetDocumentResponse._from_data(resp.json())
