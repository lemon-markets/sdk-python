from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional

from lemon.helpers import Environment

Plan = Literal["go", "investor", "trader"]


@dataclass
class Account:
    created_at: datetime
    account_id: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    billing_address: Optional[str]
    billing_email: Optional[str]
    billing_name: Optional[str]
    billing_vat: Optional[str]
    mode: Optional[Environment]
    deposit_id: Optional[str]
    client_id: Optional[str]
    account_number: Optional[str]
    iban_brokerage: Optional[str]
    iban_origin: Optional[str]
    bank_name_origin: Optional[str]
    balance: Optional[int]
    cash_to_invest: Optional[int]
    cash_to_withdraw: Optional[int]
    amount_bought_intraday: Optional[int]
    amount_sold_intraday: Optional[int]
    amount_open_orders: Optional[int]
    amount_open_withdrawals: Optional[int]
    amount_estimate_taxes: Optional[int]
    approved_at: Optional[datetime]
    trading_plan: Plan
    data_plan: Plan
    tax_allowance: Optional[int]
    tax_allowance_start: Optional[date]
    tax_allowance_end: Optional[date]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Account":
        return Account(
            created_at=datetime.fromisoformat(data["created_at"]),
            account_id=data["account_id"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
            billing_address=data["billing_address"],
            billing_email=data["billing_email"],
            billing_name=data["billing_name"],
            billing_vat=data["billing_vat"],
            mode=data["mode"],
            deposit_id=data["deposit_id"],
            client_id=data["client_id"],
            account_number=data["account_number"],
            iban_brokerage=data["iban_brokerage"],
            iban_origin=data["iban_origin"],
            bank_name_origin=data["bank_name_origin"],
            balance=int(data["balance"]) if data["balance"] is not None else None,
            cash_to_invest=int(data["cash_to_invest"])
            if data["cash_to_invest"] is not None
            else None,
            cash_to_withdraw=int(data["cash_to_withdraw"])
            if data["cash_to_withdraw"] is not None
            else None,
            amount_bought_intraday=int(data["amount_bought_intraday"])
            if data["amount_bought_intraday"] is not None
            else None,
            amount_sold_intraday=int(data["amount_sold_intraday"])
            if data["amount_sold_intraday"] is not None
            else None,
            amount_open_orders=int(data["amount_open_orders"])
            if data["amount_open_orders"] is not None
            else None,
            amount_open_withdrawals=int(data["amount_open_withdrawals"])
            if data["amount_open_withdrawals"] is not None
            else None,
            amount_estimate_taxes=int(data["amount_estimate_taxes"])
            if data["amount_estimate_taxes"] is not None
            else None,
            approved_at=datetime.fromisoformat(data["approved_at"])
            if data["approved_at"] is not None
            else None,
            trading_plan=data["trading_plan"],
            data_plan=data["data_plan"],
            tax_allowance=data["tax_allowance"],
            tax_allowance_start=datetime.fromisoformat(
                data["tax_allowance_start"]
            ).date()
            if data["tax_allowance_start"] is not None
            else None,
            tax_allowance_end=datetime.fromisoformat(data["tax_allowance_end"]).date()
            if data["tax_allowance_end"] is not None
            else None,
        )


@dataclass
class GetAccountResponse:
    time: datetime
    mode: Environment
    results: Account

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetAccountResponse":
        return GetAccountResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=Account._from_data(data["results"]),
        )


@dataclass
class Withdrawal:
    id: str
    amount: int
    created_at: datetime
    date: Optional[date]
    idempotency: Optional[str]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Withdrawal":
        return Withdrawal(
            id=data["id"],
            amount=int(data["amount"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            date=datetime.fromisoformat(data["date"]).date()
            if data["date"] is not None
            else None,
            idempotency=data["idempotency"],
        )


@dataclass
class GetWithdrawalsResponse:
    time: datetime
    mode: Environment
    results: List[Withdrawal]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetWithdrawalsResponse":
        return GetWithdrawalsResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[Withdrawal._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )


@dataclass
class WithdrawResponse:
    time: datetime
    mode: Environment

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "WithdrawResponse":
        return WithdrawResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
        )


BankStatementType = Literal[
    "pay_in",
    "pay_out",
    "order_buy",
    "order_sell",
    "dividend",
    "tax_refund",
    "interest_paid",
    "interest_earned",
    "eod_balance",
]


@dataclass
class BankStatement:
    id: str
    account_id: str
    type: BankStatementType
    date: date
    amount: int
    isin: Optional[str]
    isin_title: Optional[str]
    created_at: datetime
    quantity: Optional[int]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "BankStatement":
        return BankStatement(
            id=data["id"],
            account_id=data["account_id"],
            type=data["type"],
            date=datetime.fromisoformat(data["date"]).date(),
            amount=int(data["amount"]),
            isin=data["isin"],
            isin_title=data["isin_title"],
            created_at=datetime.fromisoformat(data["created_at"]),
            quantity=int(data["quantity"]) if data["quantity"] is not None else None,
        )


@dataclass
class GetBankStatementsResponse:
    time: datetime
    mode: Environment
    results: List[BankStatement]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetBankStatementsResponse":
        return GetBankStatementsResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[BankStatement._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )


@dataclass
class Document:
    id: str
    name: str
    created_at: datetime
    category: str
    link: str
    viewed_first_at: Optional[datetime]
    viewed_last_at: Optional[datetime]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Document":
        return Document(
            id=data["id"],
            name=data["name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            category=data["category"],
            link=data["link"],
            viewed_first_at=datetime.fromisoformat(data["viewed_first_at"])
            if data["viewed_first_at"] is not None
            else None,
            viewed_last_at=datetime.fromisoformat(data["viewed_last_at"])
            if data["viewed_last_at"] is not None
            else None,
        )


@dataclass
class GetDocumentsResponse:
    time: datetime
    mode: Environment
    results: List[Document]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetDocumentsResponse":
        return GetDocumentsResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=[Document._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )


@dataclass
class DocumentUrl:
    public_url: Optional[str]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "DocumentUrl":
        return DocumentUrl(public_url=data["public_url"])


@dataclass
class GetDocumentResponse:
    time: datetime
    mode: Environment
    results: DocumentUrl

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetDocumentResponse":
        return GetDocumentResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=DocumentUrl._from_data(data["results"]),
        )
