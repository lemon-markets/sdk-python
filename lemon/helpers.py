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
Environment = Literal["paper", "money"]
Plan = Literal["go", "investor", "trader"]


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

        self._handle_common_errors(resp)
        return resp

    def put(self, url: str, data: Any) -> requests.Response:
        url = urljoin(self._base_url, url)
        resp = requests.put(
            url,
            json=data,
            headers={"Authorization": f"Bearer {self._config.api_token}"},
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def post(self, url: str, data: Any) -> requests.Response:
        url = urljoin(self._base_url, url)
        resp = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Bearer {self._config.api_token}"},
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def delete(self, url: str) -> requests.Response:
        url = urljoin(self._base_url, url)
        resp = requests.delete(
            url,
            headers={"Authorization": f"Bearer {self._config.api_token}"},
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def _handle_common_errors(self, response: requests.Response) -> None:
        error = response.json()
        error_code = error["error_code"]
        if error_code == ErrorCodes.UNAUTHORIZED:
            raise AuthenticationError._from_data(error)
        if error_code == ErrorCodes.INTERNAL_ERROR:
            raise InternalServerError._from_data(error)
        if error_code == ErrorCodes.INVALID_QUERY:
            raise InvalidQueryError._from_data(error)
