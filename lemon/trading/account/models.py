from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict

from lemon.helpers import Environment, Plan


@dataclass
class Account:
    created_at: datetime
    account_id: str
    firstname: str
    lastname: str
    email: str
    phone: str
    address: str
    billing_address: str
    billing_email: str
    billing_name: str
    billing_vat: str
    mode: Environment
    deposit_id: str
    client_id: str
    account_number: str
    iban_brokerage: str
    iban_origin: str
    bank_name_origin: str
    balance: int
    cash_to_invest: int
    cash_to_withdraw: int
    amount_bought_intraday: int
    amount_sold_intraday: int
    amount_open_orders: int
    amount_open_withdrawals: int
    amount_estimate_taxes: int
    approved_at: datetime
    trading_plan: Plan
    data_plan: Plan
    tax_allowance: int
    tax_allowance_start: date
    tax_allowance_end: date

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
            balance=int(data["balance"]),
            cash_to_invest=int(data["cash_to_invest"]),
            cash_to_withdraw=int(data["cash_to_withdraw"]),
            amount_bought_intraday=int(data["amount_bought_intraday"]),
            amount_sold_intraday=int(data["amount_sold_intraday"]),
            amount_open_orders=int(data["amount_open_orders"]),
            amount_open_withdrawals=int(data["amount_open_withdrawals"]),
            amount_estimate_taxes=int(data["amount_estimate_taxes"]),
            approved_at=datetime.fromisoformat(data["approved_at"]),
            trading_plan=data["trading_plan"],
            data_plan=data["data_plan"],
            tax_allowance=data["tax_allowance"],
            tax_allowance_start=datetime.fromisoformat(
                data["tax_allowance_start"]
            ).date(),
            tax_allowance_end=datetime.fromisoformat(data["tax_allowance_end"]).date(),
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
