import enum
from datetime import datetime
from typing import Any, Dict, Type, TypeVar

TApiError = TypeVar("TApiError", bound="ApiError")


class ErrorCodes(str, enum.Enum):
    UNAUTHORIZED = "unauthorized"
    ENTITY_NOT_FOUND = "entity_not_found"
    INTERNAL_ERROR = "internal_error"
    INVALID_QUERY = "invalid_query"
    UNKNOWN_ERROR = "unknown_error"


class BaseError(Exception):
    pass


class ApiError(BaseError):
    def __init__(self, time: datetime, error_code: ErrorCodes, error_message: str):
        super().__init__(time, error_code, error_message)
        self.time = time
        self.error_code = error_code
        self.error_message = error_message

    @classmethod
    def _from_data(cls: Type[TApiError], data: Dict[str, str]) -> TApiError:
        return cls(
            time=datetime.fromisoformat(data["time"]),
            error_code=ErrorCodes(data["error_code"]),
            error_message=data["error_message"],
        )


class AuthenticationError(ApiError):
    pass


class EntityNotFoundError(ApiError):
    ERROR_SUFFIX = "_not_found"

    def __init__(
        self, time: datetime, error_code: ErrorCodes, error_message: str, entity: str
    ):
        super().__init__(time, error_code, error_message)
        self.entity = entity

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "EntityNotFoundError":
        return cls(
            time=datetime.fromisoformat(data["time"]),
            error_code=ErrorCodes.ENTITY_NOT_FOUND,
            error_message=data["error_message"],
            entity=data["error_code"][: -len(cls.ERROR_SUFFIX)],
        )


class InternalServerError(ApiError):
    pass


class InvalidQueryError(ApiError):
    pass


class UnknownError(BaseError):
    def __init__(self, data: Any):
        super().__init__(data)
        self.data = data

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "UnknownError":
        return cls(data=data)


class TradingErrorCodes(str, enum.Enum):
    ACCOUNT_INSUFFICIENT_FUNDS = "account_insufficient_funds"
    FORBIDDEN_FOR_VENUE = "forbidden_for_venue"
    FORBIDDEN_IN_CURRENT_STATE = "forbidden_in_current_state"
    INSTRUMENT_NOT_TRADABLE = "instrument_not_tradable"
    INSUFFICIENT_HOLDINGS = "insufficient_holdings"
    ORDER_EXPIRATION_DATE_INVALID = "order_expiration_date_invalid"
    ORDER_IDEMPOTENCY_VIOLATION = "order_idempotency_violation"
    ORDER_LIMIT_EXCEEDED = "order_limit_exceeded"
    ORDER_NOT_INACTIVE = "order_not_inactive"
    ORDER_NOT_TERMINATED = "order_not_terminated"
    ORDER_TOTAL_PRICE_LIMIT_EXCEEDED = "order_total_price_limit_exceeded"
    PIN_INVALID = "pin_invalid"
    PIN_MISSING = "pin_missing"
    PIN_NOT_SET = "pin_not_set"
    PLAN_NOT_ALLOWED = "plan_not_allowed"
    TRADING_BLOCKED = "trading_blocked"
    TRADING_DISABLED = "trading_disabled"
    WITHDRAW_IDEMPOTENCY_VIOLATION = "withdraw_idempotency_violation"
    WITHDRAW_INSUFFICIENT_FUNDS = "withdraw_insufficient_funds"
    WITHDRAW_LIMIT_EXCEEDED = "withdraw_limit_exceeded"
    WITHDRAW_REQUEST_LIMIT_EXCEEDED = "withdraw_request_limit_exceeded"

    # FORBIDDEN_FOR_USER = "forbidden_for_user"
    # KEY_LIMIT_EXCEEDED = "key_limit_exceeded"
    # NOT_EXISTS = "not_exists"
    # ORDER_TOTAL_PRICE_TOO_LOW = "order_total_price_too_low"
    # RISK_LIMIT_LT_BACKFIRE = "risk_limit_lt_backfire"
    # TOKEN_INVALID = "token_invalid"
    # USER_NOT_ALLOWED = "user_not_allowed"


class TradingApiError(BaseError):
    def __init__(
        self, time: datetime, error_code: TradingErrorCodes, error_message: str
    ):
        super().__init__(time, error_code, error_message)
        self.time = time
        self.error_code = error_code
        self.error_message = error_message

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "TradingApiError":
        return cls(
            time=datetime.fromisoformat(data["time"]),
            error_code=TradingErrorCodes(data["error_code"]),
            error_message=data["error_message"],
        )
