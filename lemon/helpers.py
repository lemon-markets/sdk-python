from typing import Union
from urllib.parse import urlencode, urljoin

import requests

from lemon.config import Config
from lemon.errors import (
    AuthenticationError,
    ErrorCodes,
    InternalServerError,
    InvalidQueryError,
    RequestsError,
)


def encode_query_string(**kwargs: Union[str, int, None]) -> str:
    params = {k: v for k, v in kwargs.items() if v is not None}
    return urlencode(params)


class ApiClient:
    def __init__(self, config: Config):
        self._config = config

    def get(self, url: str) -> requests.Response:
        url = urljoin(self._config.api_url, url)
        try:
            resp = requests.get(
                url, headers={"Authorization": f"Bearer {self._config.api_token}"}
            )
        except requests.exceptions.RequestException as exc:
            raise RequestsError(cause=exc) from exc

        if resp.ok:
            return resp

        error = resp.json()
        error_code = error["error_code"]
        if error_code == ErrorCodes.UNAUTHORIZED:
            raise AuthenticationError._from_data(error)
        if error_code == ErrorCodes.INVALID_TOKEN:
            raise AuthenticationError._from_data(error)
        if error_code == ErrorCodes.INTERNAL_ERROR:
            raise InternalServerError._from_data(error)
        if error_code == ErrorCodes.INVALID_QUERY:
            raise InvalidQueryError._from_data(error)

        return resp
