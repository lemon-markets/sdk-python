import abc
from typing import Dict, Generator

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.errors import (
    APIError,
    AuthenticationError,
    BusinessLogicError,
    InternalServerError,
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


@pytest.fixture(scope="session")
def streaming_httpserver() -> Generator[HTTPServer, None, None]:
    yield from make_http_server()


@pytest.fixture(autouse=True)
def clear_stubs_queue(
    market_data_httpserver: HTTPServer, trading_httpserver: HTTPServer
):
    yield

    assert len(market_data_httpserver.oneshot_handlers) == 0
    market_data_httpserver.check_assertions()
    market_data_httpserver.clear()

    assert len(trading_httpserver.oneshot_handlers) == 0
    trading_httpserver.check_assertions()
    trading_httpserver.clear()


@pytest.fixture
def client(
    market_data_httpserver: HTTPServer,
    streaming_httpserver: HTTPServer,
    trading_httpserver: HTTPServer,
) -> Api:
    return Api(
        market_data_api_token="foobar",
        trading_api_token="barbaz",
        market_data_api_url=market_data_httpserver.url_for(""),
        streaming_api_url=streaming_httpserver.url_for(""),
        trading_api_url=trading_httpserver.url_for(""),
        timeout=1,
        retry_count=1,
        retry_backoff_factor=1,
    )


class CommonApiTests:
    @abc.abstractmethod
    def make_api_call(self, client: Api, **params) -> None:
        ...

    def test_handle_unauthorized_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error("unauthorized"), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)

    def test_handle_token_invalid_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error("token_invalid"), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)

    def test_handle_entity_not_found_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error("account_not_found"), status=400
        )
        with pytest.raises(BusinessLogicError):
            self.make_api_call(client)

    def test_handle_internal_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error("internal_error"), status=400
        )
        with pytest.raises(InternalServerError):
            self.make_api_call(client)

    def test_handle_unknown_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            {"foo": "bar"}, status=400
        )
        with pytest.raises(APIError):
            self.make_api_call(client)
