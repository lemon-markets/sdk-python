from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from lemon.types import BaseModel, Environment


@dataclass
class User(BaseModel):
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


@dataclass
class GetUserResponse(BaseModel):
    time: datetime
    mode: Environment
    results: User
