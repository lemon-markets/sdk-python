import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.errors import TradingApiError, TradingErrorCodes
from tests.conftest import CommonApiTests, build_error


class CommonTradingApiTests(CommonApiTests):
    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    def test_handle_trading_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error(TradingErrorCodes.PIN_INVALID.value), status=400
        )
        with pytest.raises(TradingApiError):
            self.make_api_call(client)
