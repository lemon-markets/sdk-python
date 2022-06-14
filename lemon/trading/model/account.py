from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from typing_extensions import Literal

from lemon.types import BaseModel, Environment, to_date, to_type

Plan = Literal["go", "investor", "trader"]


@dataclass
class Account(BaseModel):
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
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            billing_address=data.get("billing_address"),
            billing_email=data.get("billing_email"),
            billing_name=data.get("billing_name"),
            billing_vat=data.get("billing_vat"),
            mode=data.get("mode"),
            deposit_id=data.get("deposit_id"),
            client_id=data.get("client_id"),
            account_number=data.get("account_number"),
            iban_brokerage=data.get("iban_brokerage"),
            iban_origin=data.get("iban_origin"),
            bank_name_origin=data.get("bank_name_origin"),
            balance=to_type(int, data.get("balance")),
            cash_to_invest=to_type(int, data.get("cash_to_invest")),
            cash_to_withdraw=to_type(int, data.get("cash_to_withdraw")),
            amount_bought_intraday=to_type(int, data.get("amount_bought_intraday")),
            amount_sold_intraday=to_type(int, data.get("amount_sold_intraday")),
            amount_open_orders=to_type(int, data.get("amount_open_orders")),
            amount_open_withdrawals=to_type(int, data.get("amount_open_withdrawals")),
            amount_estimate_taxes=to_type(int, data.get("amount_estimate_taxes")),
            approved_at=to_type(datetime.fromisoformat, data.get("approved_at")),
            trading_plan=data["trading_plan"],
            data_plan=data["data_plan"],
            tax_allowance=to_type(int, data.get("tax_allowance")),
            tax_allowance_start=to_type(to_date, data.get("tax_allowance_start")),
            tax_allowance_end=to_type(to_date, data.get("tax_allowance_end")),
        )


@dataclass
class GetAccountResponse(BaseModel):
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
class Withdrawal(BaseModel):
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
            date=to_type(to_date, data.get("date")),
            idempotency=data.get("idempotency"),
        )


@dataclass
class GetWithdrawalsResponse(BaseModel):
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
class WithdrawResponse(BaseModel):
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
class BankStatement(BaseModel):
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
            isin=data.get("isin"),
            isin_title=data.get("isin_title"),
            created_at=datetime.fromisoformat(data["created_at"]),
            quantity=to_type(int, data.get("quantity")),
        )


@dataclass
class GetBankStatementsResponse(BaseModel):
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
class Document(BaseModel):
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
            viewed_first_at=to_type(
                datetime.fromisoformat, data.get("viewed_first_at")
            ),
            viewed_last_at=to_type(datetime.fromisoformat, data.get("viewed_last_at")),
        )


@dataclass
class GetDocumentsResponse(BaseModel):
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
class DocumentUrl(BaseModel):
    public_url: Optional[str]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "DocumentUrl":
        return DocumentUrl(public_url=data.get("public_url"))


@dataclass
class GetDocumentResponse(BaseModel):
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
