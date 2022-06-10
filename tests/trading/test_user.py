from datetime import date, datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.model import GetUserResponse, User
from tests.trading.conftest import CommonTradingApiTests

DUMMY_USER_PAYLOAD = {
    "time": "2022-06-01T18:37:03.817",
    "mode": "paper",
    "status": "ok",
    "results": {
        "created_at": "2022-06-01T18:37:03.817",
        "user_id": "string",
        "firstname": "string",
        "lastname": "string",
        "email": "string",
        "phone": "string",
        "phone_verified": "2022-06-01T18:37:03.817",
        "pin_verified": True,
        "account_id": "string",
        "trading_plan": "string",
        "data_plan": "string",
        "tax_allowance": 0,
        "tax_allowance_start": "2022-06-01",
        "tax_allowance_end": "2022-06-01",
        "optin_order_push": True,
        "optin_order_email": True,
        "country": "string",
        "language": "string",
        "timezone": "string",
    },
}

DUMMY_USER_RESPONSE = GetUserResponse(
    time=datetime.fromisoformat("2022-06-01T18:37:03.817"),
    mode="paper",
    results=User(
        created_at=datetime.fromisoformat("2022-06-01T18:37:03.817"),
        user_id="string",
        firstname="string",
        lastname="string",
        email="string",
        phone="string",
        phone_verified=datetime.fromisoformat("2022-06-01T18:37:03.817"),
        pin_verified=True,
        account_id="string",
        trading_plan="string",
        data_plan="string",
        tax_allowance=0,
        tax_allowance_start=date(year=2022, month=6, day=1),
        tax_allowance_end=date(year=2022, month=6, day=1),
        optin_order_push=True,
        optin_order_email=True,
        country="string",
        language="string",
        timezone="string",
    ),
)


class TestGetUserApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.user.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/user", "method": "GET"}

    def test_get_user(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/user",
            method="GET",
        ).respond_with_json(DUMMY_USER_PAYLOAD)
        assert client.trading.user.get() == DUMMY_USER_RESPONSE

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/user",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/user",
            method="GET",
        ).respond_with_json(DUMMY_USER_PAYLOAD)

        assert client.trading.user.get() == DUMMY_USER_RESPONSE
