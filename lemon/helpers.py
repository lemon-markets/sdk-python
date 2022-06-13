import json
from dataclasses import asdict
from datetime import date, datetime, time
from functools import wraps
from typing import Any, Callable, Dict, Literal, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

from lemon.config import Config
from lemon.errors import (
    AuthenticationError,
    BusinessLogicError,
    InternalServerError,
    InvalidRequestError,
    UnexpectedError,
)

Sorting = Literal["asc", "desc"]
Environment = Literal["paper", "money"]
Days = int


def as_or_none(type_: Callable[[Any], Any], value: Any) -> Any:
    return type_(value) if value is not None else None


def to_date(x: str) -> date:
    return datetime.fromisoformat(x).date()


class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        return super().default(o)


class BaseModel:
    def dict(self) -> Dict[str, Any]:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(asdict(self), cls=JSONEncoder)


def handle_errors(response: requests.Response) -> None:
    error = response.json()
    error_code: Optional[str] = error.get("error_code")
    if error_code is None:
        raise UnexpectedError._from_data(error)
    if error_code == "invalid_request":
        raise InvalidRequestError._from_data(error)
    if error_code == "internal_error":
        raise InternalServerError._from_data(error)
    if error_code in ["unauthorized", "token_invalid"]:
        raise AuthenticationError._from_data(error)

    raise BusinessLogicError._from_data(error)


def _handle_error(
    func: Callable[..., requests.Response]
) -> Callable[..., requests.Response]:
    @wraps(func)
    def inner(*arg: Any, **kwargs: Any) -> requests.Response:
        response = func(*arg, **kwargs)
        if not response.ok:
            handle_errors(response)
        return response

    return inner


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
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
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
            json=json,
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
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
            json=json,
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
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
            params=params,
            headers={"Authorization": f"Bearer {self._config.api_token}", **headers},
            timeout=self._config.timeout,
        )
