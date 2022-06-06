import pytest
from pytest_httpserver import HTTPServer

from tests.conftest import CommonApiTests


class CommonMarketDataApiTests(CommonApiTests):
    @pytest.fixture
    def httpserver(self, market_data_httpserver: HTTPServer):
        return market_data_httpserver
