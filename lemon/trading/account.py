from datetime import date
from typing import Literal, Optional, Union

from lemon.helpers import ApiClient, Sorting, handle_trading_errors
from lemon.trading.model import (
    BankStatementType,
    GetAccountResponse,
    GetBankStatementsResponse,
    GetDocumentResponse,
    GetDocumentsResponse,
    GetWithdrawalsResponse,
    WithdrawResponse,
)


class Account:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(self) -> GetAccountResponse:
        resp = self._client.get("account")
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
        return GetDocumentsResponse._from_data(resp.json())

    def get_document(
        self, document_id: str, no_redirect: Optional[bool] = None
    ) -> GetDocumentResponse:
        resp = self._client.get(
            f"account/documents/{document_id}",
            params={"no_redirect": no_redirect},
        )
        if not resp.ok:
            handle_trading_errors(resp.json())
        return GetDocumentResponse._from_data(resp.json())
