from datetime import date, datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.account.models import (
    Account,
    GetAccountResponse,
    GetWithdrawalsResponse,
    Withdrawal,
)
from tests.conftest import CommonApiTests

DUMMY_ACCOUNT_PAYLOAD = {
    "time": "2021-11-22T15:37:56.520+00:00",
    "status": "ok",
    "mode": "paper",
    "results": {
        "created_at": "2021-10-12T10:29:49.769+00:00",
        "account_id": "acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
        "firstname": "Michael",
        "lastname": "Burry",
        "email": "m_burry@tradingapi.com",
        "phone": "+491637876521",
        "address": "Ritterstraße 2A 10969 Berlin",
        "billing_address": "Ritterstraße 2A 10969 Berlin",
        "billing_email": "m_burry@tradingapi.com",
        "billing_name": "Michael Burry",
        "billing_vat": "DE999999999",
        "mode": "paper",
        "deposit_id": "K2057263187",
        "client_id": "2057263",
        "account_number": "2057263187",
        "iban_brokerage": "DE12345678902057263",
        "iban_origin": "DE123456789012345",
        "bank_name_origin": "Test Bank",
        "balance": 100000000,
        "cash_to_invest": 80000000,
        "cash_to_withdraw": 20000000,
        "amount_bought_intraday": 0,
        "amount_sold_intraday": 0,
        "amount_open_orders": 0,
        "amount_open_withdrawals": 1475200,
        "amount_estimate_taxes": 0,
        "approved_at": "2021-11-19T07:40:12.563+00:00",
        "trading_plan": "investor",
        "data_plan": "investor",
        "tax_allowance": 8010000,
        "tax_allowance_start": "2021-01-01",
        "tax_allowance_end": "2021-01-01",
    },
}

DUMMY_WITHDRAWLS_PAYLOAD = {
    "time": "2021-12-15T11:21:21.023+00:00",
    "status": "ok",
    "mode": "paper",
    "results": [
        {
            "id": "wtd_pyQTPbbLLMNBQTM0mzkK7Ygb8kH60Ff10X",
            "amount": 1000000,
            "created_at": "2021-12-15T11:21:05.853+00:00",
            "date": "2021-12-15T23:12:02.765+00:00",
            "idempotency": "1234abcd",
        },
    ],
    "previous": "https://paper-trading.lemon.markets/v1/account/withdrawals/?limit=20&page=1",
    "next": "https://paper-trading.lemon.markets/v1/account/withdrawals/?limit=2&page=3",
    "total": 80,
    "page": 2,
    "pages": 4,
}

DUMMY_ACCOUNT_RESPONSE = GetAccountResponse(
    time=datetime.fromisoformat("2021-11-22T15:37:56.520+00:00"),
    mode="paper",
    results=Account(
        created_at=datetime.fromisoformat("2021-10-12T10:29:49.769+00:00"),
        account_id="acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
        firstname="Michael",
        lastname="Burry",
        email="m_burry@tradingapi.com",
        phone="+491637876521",
        address="Ritterstraße 2A 10969 Berlin",
        billing_address="Ritterstraße 2A 10969 Berlin",
        billing_email="m_burry@tradingapi.com",
        billing_name="Michael Burry",
        billing_vat="DE999999999",
        mode="paper",
        deposit_id="K2057263187",
        client_id="2057263",
        account_number="2057263187",
        iban_brokerage="DE12345678902057263",
        iban_origin="DE123456789012345",
        bank_name_origin="Test Bank",
        balance=100000000,
        cash_to_invest=80000000,
        cash_to_withdraw=20000000,
        amount_bought_intraday=0,
        amount_sold_intraday=0,
        amount_open_orders=0,
        amount_open_withdrawals=1475200,
        amount_estimate_taxes=0,
        approved_at=datetime.fromisoformat("2021-11-19T07:40:12.563+00:00"),
        trading_plan="investor",
        data_plan="investor",
        tax_allowance=8010000,
        tax_allowance_start=date(year=2021, month=1, day=1),
        tax_allowance_end=date(year=2021, month=1, day=1),
    ),
)

DUMMY_WITHDRAWLS_RESPONSE = GetWithdrawalsResponse(
    time=datetime.fromisoformat("2021-12-15T11:21:21.023+00:00"),
    mode="paper",
    results=[
        Withdrawal(
            id="wtd_pyQTPbbLLMNBQTM0mzkK7Ygb8kH60Ff10X",
            amount=1000000,
            created_at=datetime.fromisoformat("2021-12-15T11:21:05.853+00:00"),
            date=datetime.fromisoformat("2021-12-15T23:12:02.765+00:00").date(),
            idempotency="1234abcd",
        )
    ],
    total=80,
    page=2,
    pages=4,
)


class TestGetAccountApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    def test_get_account(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_request(
            "/account",
            method="GET",
        ).respond_with_json(DUMMY_ACCOUNT_PAYLOAD)
        assert client.trading.account.get() == DUMMY_ACCOUNT_RESPONSE


class TestEditAccountApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.update({"address_street": "new street"})

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/account",
            "method": "PUT",
            "json": {"address_street": "new street"},
        }

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    def test_get_account(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_request(
            "/account",
            method="PUT",
            json={"address_street": "new street"},
        ).respond_with_json(DUMMY_ACCOUNT_PAYLOAD)
        assert (
            client.trading.account.update({"address_street": "new street"})
            == DUMMY_ACCOUNT_RESPONSE
        )


class TestGetWithdrawalsApi(CommonApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get_withdrawals()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account/withdrawals", "method": "GET"}

    @pytest.fixture
    def httpserver(self, trading_httpserver: HTTPServer):
        return trading_httpserver

    def test_get_withdrawals(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_request(
            "/account/withdrawals",
            method="GET",
        ).respond_with_json(DUMMY_WITHDRAWLS_PAYLOAD)
        assert client.trading.account.get_withdrawals() == DUMMY_WITHDRAWLS_RESPONSE
