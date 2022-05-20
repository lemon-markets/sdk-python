import enum
from datetime import datetime
from typing import Dict, Type, TypeVar

import requests

TApiError = TypeVar("TApiError", bound="ApiError")


class ErrorCodes(str, enum.Enum):
    UNAUTHORIZED = "unauthorized"
    INVALID_TOKEN = "token_invalid"
    INTERNAL_ERROR = "internal_error"
    INVALID_QUERY = "invalid_query"


class BaseError(Exception):
    pass


class RequestsError(BaseError):
    def __init__(self, cause: requests.RequestException):
        super().__init__(cause)
        self.cause = cause


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


class InternalServerError(ApiError):
    pass


class InvalidQueryError(ApiError):
    pass
