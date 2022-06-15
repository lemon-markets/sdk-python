from datetime import datetime
from typing import Any, Dict


class BaseLemonError(Exception):
    """Base class for all lemon.markets errors."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class LemonError(BaseLemonError):
    def __init__(self, time: datetime, error_code: str, error_message: str):
        super().__init__(time, error_code, error_message)
        self.time = time
        self.error_code = error_code
        self.error_message = error_message

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "LemonError":
        return cls(
            time=datetime.fromisoformat(data["time"]),
            error_code=data["error_code"],
            error_message=data["error_message"],
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"("
            f"time={self.time.isoformat()}, "
            f"error_code={self.error_code}, "
            f"error_message={self.error_message}"
            f")"
        )


class InvalidQueryError(LemonError):
    ...


class AuthenticationError(LemonError):
    ...


class InternalServerError(LemonError):
    ...


class BusinessLogicError(LemonError):
    ...


class APIError(BaseLemonError):
    def __init__(self, data: Any):
        super().__init__(data)
        self.data = data

    @classmethod
    def _from_data(cls, data: Dict[str, str]) -> "APIError":
        return cls(data=data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self.data})"
