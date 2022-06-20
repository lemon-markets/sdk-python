from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

from typing_extensions import Literal

from lemon.types import BaseModel, Environment

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


@dataclass
class GetAccountResponse(BaseModel):
    time: datetime
    mode: Environment
    results: Account


@dataclass
class Withdrawal(BaseModel):
    id: str
    amount: int
    created_at: datetime
    date: Optional[date]
    idempotency: Optional[str]


@dataclass
class GetWithdrawalsResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Withdrawal]
    total: int
    page: int
    pages: int


@dataclass
class WithdrawResponse(BaseModel):
    time: datetime
    mode: Environment


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


@dataclass
class GetBankStatementsResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[BankStatement]
    total: int
    page: int
    pages: int


@dataclass
class Document(BaseModel):
    id: str
    name: str
    created_at: datetime
    category: str
    link: str
    viewed_first_at: Optional[datetime]
    viewed_last_at: Optional[datetime]


@dataclass
class GetDocumentsResponse(BaseModel):
    time: datetime
    mode: Environment
    results: List[Document]
    total: int
    page: int
    pages: int


@dataclass
class DocumentUrl(BaseModel):
    public_url: Optional[str]


@dataclass
class GetDocumentResponse(BaseModel):
    time: datetime
    mode: Environment
    results: DocumentUrl
