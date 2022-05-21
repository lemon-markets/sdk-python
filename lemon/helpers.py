from typing import Any, Dict, Literal, Optional
from urllib.parse import urljoin

import requests

from lemon.config import Config
from lemon.errors import (
    AuthenticationError,
    ErrorCodes,
    InternalServerError,
    InvalidQueryError,
)

Sorting = Literal["asc", "desc"]


class ApiClient:
    def __init__(self, base_url: str, config: Config):
        self._base_url = base_url
        self._config = config

    def get(
        self, url: str, query_params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        resp = requests.get(
            url,
            params=query_params,
            headers={"Authorization": f"Bearer {self._config.api_token}"},
        )

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
