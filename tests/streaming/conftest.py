import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.errors import AuthenticationError
from tests.conftest import CommonApiTests, build_error


class CommonStreamingAPITests(CommonApiTests):
    @pytest.fixture
    def httpserver(self, streaming_httpserver: HTTPServer):
        return streaming_httpserver

    def test_handle_streaming_error(
        self, client: Api, httpserver: HTTPServer, api_call_kwargs
    ):
        httpserver.expect_oneshot_request(**api_call_kwargs).respond_with_json(
            build_error("token_invalid"), status=400
        )
        with pytest.raises(AuthenticationError):
            self.make_api_call(client)
