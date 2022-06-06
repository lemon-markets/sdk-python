import pytest
from pytest_httpserver import HTTPServer

from tests.conftest import CommonApiTests


class CommonTradingApiTests(CommonApiTests):
    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver
