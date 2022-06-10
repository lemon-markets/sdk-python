from datetime import date, datetime
from typing import Any, Callable, Dict, Literal, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

from lemon.config import Config
from lemon.errors import (
    AuthenticationError,
    ErrorCodes,
    InternalServerError,
    InvalidQueryError,
)

Sorting = Literal["asc", "desc"]
Environment = Literal["paper", "money"]
Days = int


class ApiClient:
    def __init__(self, base_url: str, config: Config):
        self._base_url = base_url
        self._config = config
        self._session = requests.Session()
        retries = Retry(
            total=config.retry_count,
            backoff_factor=config.retry_backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "DELETE", "OPTIONS", "TRACE"],
        )

        self._session.mount("http://", HTTPAdapter(max_retries=retries))
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        resp = self._session.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def put(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        resp = self._session.put(
            url,
            json=json,
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def post(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        resp = self._session.post(
            url,
            json=json,
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def delete(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        resp = self._session.delete(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
        )

        if resp.ok:
            return resp

        self._handle_common_errors(resp)
        return resp

    def _handle_common_errors(self, response: requests.Response) -> None:
        error = response.json()
        error_code = error.get("error_code")
        if error_code == ErrorCodes.UNAUTHORIZED:
            raise AuthenticationError._from_data(error)
        if error_code == ErrorCodes.INTERNAL_ERROR:
            raise InternalServerError._from_data(error)
        if error_code == ErrorCodes.INVALID_QUERY:
            raise InvalidQueryError._from_data(error)


def as_or_none(type_: Callable[[Any], Any], value: Any) -> Any:
    return type_(value) if value is not None else None


def to_date(x: str) -> date:
    return datetime.fromisoformat(x).date()
