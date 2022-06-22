from functools import wraps
from typing import Any, Callable, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry
from typing_extensions import ParamSpec

from lemon.errors import (
    APIError,
    AuthenticationError,
    BusinessLogicError,
    InternalServerError,
    InvalidQueryError,
)
from lemon.types import filter_out_optionals

P = ParamSpec("P")


def _handle_error(
    func: Callable[P, requests.Response]
) -> Callable[P, requests.Response]:
    @wraps(func)
    def inner(*arg: P.args, **kwargs: P.kwargs) -> requests.Response:
        response = func(*arg, **kwargs)
        if not response.ok:
            error = response.json()
            error_code: Optional[str] = error.get("error_code")
            if error_code is None:
                raise APIError._from_data(error)
            if error_code == "invalid_query":
                raise InvalidQueryError._from_data(error)
            if error_code == "internal_error":
                raise InternalServerError._from_data(error)
            if error_code in ["unauthorized", "token_invalid"]:
                raise AuthenticationError._from_data(error)

            raise BusinessLogicError._from_data(error)

        return response

    return inner


class Client:
    def __init__(
        self,
        base_url: str,
        api_token: str,
        timeout: float,
        retry_count: int,
        retry_backoff_factor: float,
    ):
        self._base_url = base_url
        self._api_token = api_token
        self._timeout = timeout
        self._session = requests.Session()
        retries = Retry(
            total=retry_count,
            backoff_factor=retry_backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "DELETE", "OPTIONS", "TRACE"],
        )

        self._session.mount("http://", HTTPAdapter(max_retries=retries))
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

    @_handle_error
    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        return self._session.get(
            url,
            params=filter_out_optionals(params) if params else None,
            headers={"Authorization": f"Bearer {self._api_token}", **headers},
            timeout=self._timeout,
        )

    @_handle_error
    def put(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        return self._session.put(
            url,
            json=filter_out_optionals(json),
            params=filter_out_optionals(params) if params else None,
            headers={"Authorization": f"Bearer {self._api_token}", **headers},
            timeout=self._timeout,
        )

    @_handle_error
    def post(
        self,
        url: str,
        json: Any,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        return self._session.post(
            url,
            json=filter_out_optionals(json),
            params=filter_out_optionals(params) if params else None,
            headers={"Authorization": f"Bearer {self._api_token}", **headers},
            timeout=self._timeout,
        )

    @_handle_error
    def delete(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = urljoin(self._base_url, url)
        headers = headers or {}
        return self._session.delete(
            url,
            params=filter_out_optionals(params) if params else None,
            headers={"Authorization": f"Bearer {self._api_token}", **headers},
            timeout=self._timeout,
        )
