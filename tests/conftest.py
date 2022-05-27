from typing import Dict, Generator

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api, create
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


def make_http_server() -> Generator[HTTPServer, None, None]:
    server = HTTPServer(
        host=HTTPServer.DEFAULT_LISTEN_HOST, port=HTTPServer.DEFAULT_LISTEN_PORT
    )
    server.start()
    yield server
    server.clear()
    if server.is_running():
        server.stop()


@pytest.fixture(scope="session")
def market_data_httpserver() -> Generator[HTTPServer, None, None]:
    yield from make_http_server()


@pytest.fixture(scope="session")
def trading_httpserver() -> Generator[HTTPServer, None, None]:
    yield from make_http_server()


@pytest.fixture(autouse=True)
def clear_stubs_queue(
    market_data_httpserver: HTTPServer, trading_httpserver: HTTPServer
):
    yield
    market_data_httpserver.clear()
    trading_httpserver.clear()


@pytest.fixture
def client(market_data_httpserver: HTTPServer, trading_httpserver: HTTPServer) -> Api:
    return create(
        api_token="foobar",
        market_data_api_url=market_data_httpserver.url_for(""),
        trading_api_url=trading_httpserver.url_for(""),
    )


class CommonApiTests:
    def make_api_call(self, client: Api) -> None:
        pass

    def test_handle_unauthorized_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.UNAUTHORIZED.value), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)

    def test_handle_invalid_token_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.INVALID_TOKEN.value), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)

    def test_handle_internal_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.INTERNAL_ERROR.value), status=400
        )
        with pytest.raises(InternalServerError):
            self.make_api_call(client)

    def test_handle_invalid_query_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_request(**api_call_kwargs).respond_with_json(
            build_error(ErrorCodes.INVALID_QUERY.value), status=400
        )
        with pytest.raises(InvalidQueryError):
            self.make_api_call(client)
