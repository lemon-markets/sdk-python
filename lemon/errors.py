from datetime import datetime
from typing import Any, Dict


class LemonMarketsError(Exception):
    def __init__(self, time: datetime, error_code: str, error_message: str):
        super().__init__(time, error_code, error_message)
        self.time = time
        self.error_code = error_code
        self.error_message = error_message

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "LemonMarketsError":
        return cls(
            time=datetime.fromisoformat(data["time"]),
            error_code=data["error_code"],
            error_message=data["error_message"],
        )


class InvalidRequestError(LemonMarketsError):
    ...


class AuthenticationError(LemonMarketsError):
    ...


class InternalServerError(LemonMarketsError):
    ...


class BusinessLogicError(LemonMarketsError):
    ...


class UnexpectedError(Exception):
    def __init__(self, data: Any):
        super().__init__(data)
        self.data = data

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "UnexpectedError":
        return cls(data=data)
