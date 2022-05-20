from typing import Any, Dict

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import LemonApi, create
from lemon.errors import (
    AuthenticationError,
    ErrorCodes,
    InternalServerError,
    InvalidQueryError,
)


def build_error(error_code: str) -> Dict[str, str]:
    return {
        "time": "2001-02-03T04:05:06.789+00:00",
        "mode": "paper",
        "status": "error",
        "error_code": error_code,
        "error_message": "generic error message",
    }


def build_query_matcher(data: Dict[str, Any]) -> Dict[str, str]:
    return {k: str(v) for k, v in data.items()}


@pytest.fixture
def client(httpserver: HTTPServer) -> LemonApi:
    return create(api_token="foobar", api_url=httpserver.url_for(""))


class CommonApiTests:
    def make_api_call(self, client: LemonApi) -> None:
        pass

    def test_handle_unauthorized_error(
        self, client: LemonApi, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.UNAUTHORIZED.value), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)

    def test_handle_invalid_token_error(
        self, client: LemonApi, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.INVALID_TOKEN.value), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)

    def test_handle_internal_error(
        self, client: LemonApi, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.INTERNAL_ERROR.value), status=400
        )
        with pytest.raises(InternalServerError):
            self.make_api_call(client)

    def test_handle_invalid_query_error(
        self, client: LemonApi, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.INVALID_QUERY.value), status=400
        )
        with pytest.raises(InvalidQueryError):
            self.make_api_call(client)
