from datetime import datetime, timezone

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.errors import APIError
from lemon.streaming.model import Token
from tests.streaming.conftest import CommonStreamingAPITests

DUMMY_PAYLOAD = {
    "token": "token123",
    "user_id": "user_123",
    "expires_at": 1657929600046,
}

DUMMY_RESPONSE = Token(
    token="token123",
    user_id="user_123",
    expires_at=datetime.fromtimestamp(1657929600046 / 1000, tz=timezone.utc),
)


class TestStreamingApi(CommonStreamingAPITests):
    def make_api_call(self, client: Api) -> Token:
        return client.streaming.authenticate()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/auth", "method": "POST"}

    def test_authenticate(
        self,
        client: Api,
        httpserver: HTTPServer,
    ):
        httpserver.expect_oneshot_request("/auth", method="post").respond_with_json(
            DUMMY_PAYLOAD
        )
        assert client.streaming.authenticate() == DUMMY_RESPONSE

    def test_fail_auth_on_invalid_datetime_format(
        self, client: Api, httpserver: HTTPServer
    ):
        payload = dict(**DUMMY_PAYLOAD)
        payload["expires_at"] = "unsupported-datetime-format"

        httpserver.expect_oneshot_request("/auth", method="post").respond_with_json(
            payload
        )
        with pytest.raises(APIError):
            client.streaming.authenticate()
