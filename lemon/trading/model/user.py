from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Optional

from lemon.helpers import Environment, as_or_none, to_date


@dataclass
class User:
    created_at: datetime
    user_id: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    phone_verified: Optional[datetime]
    pin_verified: bool
    account_id: str
    trading_plan: str
    data_plan: str
    tax_allowance: Optional[int]
    tax_allowance_start: Optional[date]
    tax_allowance_end: Optional[date]
    optin_order_push: bool
    optin_order_email: bool
    country: str
    language: str
    timezone: str

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "User":
        return User(
            created_at=datetime.fromisoformat(data["created_at"]),
            user_id=data["user_id"],
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            email=data.get("email"),
            phone=data.get("phone"),
            phone_verified=as_or_none(
                datetime.fromisoformat, data.get("phone_verified")
            ),
            pin_verified=data["pin_verified"],
            account_id=data["account_id"],
            trading_plan=data["trading_plan"],
            data_plan=data["data_plan"],
            tax_allowance=data.get("tax_allowance"),
            tax_allowance_start=as_or_none(to_date, data.get("tax_allowance_start")),
            tax_allowance_end=as_or_none(to_date, data.get("tax_allowance_end")),
            optin_order_push=data["optin_order_push"],
            optin_order_email=data["optin_order_email"],
            country=data["country"],
            language=data["language"],
            timezone=data["timezone"],
        )


@dataclass
class GetUserResponse:
    time: datetime
    mode: Environment
    results: User

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetUserResponse":
        return GetUserResponse(
            time=datetime.fromisoformat(data["time"]),
            mode=data["mode"],
            results=User._from_data(data["results"]),
        )
