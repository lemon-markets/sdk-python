import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.errors import MarketDataApiError, MarketDataErrorCodes
from tests.conftest import CommonApiTests, build_error


class CommonMarketDataApiTests(CommonApiTests):
    @pytest.fixture
    def httpserver(self, market_data_httpserver: HTTPServer):
        return market_data_httpserver

    def test_handle_market_data_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error(MarketDataErrorCodes.INVALID_QUERY.value), status=400
        )
        with pytest.raises(MarketDataApiError):
            self.make_api_call(client)
