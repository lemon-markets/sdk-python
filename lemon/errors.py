from typing import Any


class LemonError(Exception):
    def __init__(self, cause: Any):
        super().__init__(cause)
        self.cause = cause


class UnexpectedError(LemonError):
    pass


class ApiError(LemonError):
    pass


class UnauthorizedError(ApiError):
    ERROR_CODE = "unauthorized"


class InvalidTokenError(ApiError):
    ERROR_CODE = "token_invalid"


class InternalServerError(ApiError):
    ERROR_CODE = "internal_error"
