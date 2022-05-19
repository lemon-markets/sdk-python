from lemon.errors import ApiError


class InvalidVenuesQuery(ApiError):
    ERROR_CODE = "invalid_query"
