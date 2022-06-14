from datetime import date, datetime

import pytest
from pytest_httpserver import HTTPServer

from lemon.api import Api
from lemon.trading.model import (
    Account,
    BankStatement,
    Document,
    DocumentUrl,
    GetAccountResponse,
    GetBankStatementsResponse,
    GetDocumentResponse,
    GetDocumentsResponse,
    GetWithdrawalsResponse,
    Withdrawal,
    WithdrawResponse,
)
from tests.trading.conftest import CommonTradingApiTests

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

DUMMY_WITHDRAW_PAYLOAD = {
    "time": "2021-11-22T15:37:56.520+00:00",
    "mode": "paper",
    "status": "ok",
}

DUMMY_BANK_STATEMENTS_PAYLOAD = {
    "time": "2021-11-22T15:41:04.028+00:00",
    "status": "ok",
    "mode": "paper",
    "results": [
        {
            "id": "bst_pyQKKTTSS0Q2drg2J7yRhTwBkMPd1JgZzZ",
            "account_id": "acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
            "type": "order_buy",
            "date": "2021-12-16",
            "amount": 100000,
            "quantity": 10,
            "isin": "US19260Q1076",
            "isin_title": "COINBASE GLOBAL INC.",
            "created_at": "2021-12-17T01:37:03.362+00:00",
        },
    ],
    "previous": "https://paper-trading.lemon.markets/v1/account/bankstatements/?limit=20&page=1",
    "next": "https://paper-trading.lemon.markets/v1/account/bankstatements/?limit=2&page=3",
    "total": 80,
    "page": 2,
    "pages": 4,
}

DUMMY_GET_DOCUMENTS_PAYLOAD = {
    "time": "2021-11-22T15:41:04.028+00:00",
    "mode": "paper",
    "status": "ok",
    "results": [
        {
            "id": "doc_pyNjNcc77ht3T3lH8dJa5fD8jhj2JHJ1xX",
            "name": "account_opening.pdf",
            "created_at": "2021-10-19T14:58:52.813",
            "category": "kyc",
            "link": "lemon.markets/v1/account/documents/doc_pyNjNcc77ht3T3lH8dJa5fD8jhj2JHJ1xX",
            "viewed_first_at": "2021-10-19T14:58:52.813",
            "viewed_last_at": "2021-10-19T14:58:52.813",
        },
    ],
    "previous": "https://paper-trading.lemon.markets/v1/account/documents/?limit=20&page=1",
    "next": "https://paper-trading.lemon.markets/v1/account/documents/?limit=2&page=3",
    "total": 80,
    "page": 2,
    "pages": 4,
}

DUMMY_GET_DOCUMENT_PAYLOAD = {
    "time": "2022-05-30T09:47:16.769",
    "mode": "paper",
    "status": "ok",
    "results": {"public_url": "foo"},
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

DUMMY_WITHDRAW_RESPONSE = WithdrawResponse(
    time=datetime.fromisoformat("2021-11-22T15:37:56.520+00:00"),
    mode="paper",
)

DUMMY_BANKSTATEMENTS_RESPONSE = GetBankStatementsResponse(
    time=datetime.fromisoformat("2021-11-22T15:41:04.028+00:00"),
    mode="paper",
    results=[
        BankStatement(
            id="bst_pyQKKTTSS0Q2drg2J7yRhTwBkMPd1JgZzZ",
            account_id="acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
            type="order_buy",
            date=date(year=2021, month=12, day=16),
            amount=100000,
            quantity=10,
            isin="US19260Q1076",
            isin_title="COINBASE GLOBAL INC.",
            created_at=datetime.fromisoformat("2021-12-17T01:37:03.362+00:00"),
        )
    ],
    total=80,
    page=2,
    pages=4,
)

DUMMY_GET_DOCUMENTS_RESPONSE = GetDocumentsResponse(
    time=datetime.fromisoformat("2021-11-22T15:41:04.028+00:00"),
    mode="paper",
    results=[
        Document(
            id="doc_pyNjNcc77ht3T3lH8dJa5fD8jhj2JHJ1xX",
            name="account_opening.pdf",
            created_at=datetime.fromisoformat("2021-10-19T14:58:52.813"),
            category="kyc",
            link="lemon.markets/v1/account/documents/doc_pyNjNcc77ht3T3lH8dJa5fD8jhj2JHJ1xX",
            viewed_first_at=datetime.fromisoformat("2021-10-19T14:58:52.813"),
            viewed_last_at=datetime.fromisoformat("2021-10-19T14:58:52.813"),
        ),
    ],
    total=80,
    page=2,
    pages=4,
)

DUMMY_GET_DOCUMENT_RESPONSE = GetDocumentResponse(
    time=datetime.fromisoformat("2022-05-30T09:47:16.769"),
    mode="paper",
    results=DocumentUrl(public_url="foo"),
)


class TestGetAccountApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account", "method": "GET"}

    def test_get_account(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account",
            method="GET",
        ).respond_with_json(DUMMY_ACCOUNT_PAYLOAD)
        assert client.trading.account.get() == DUMMY_ACCOUNT_RESPONSE

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/account",
            method="GET",
        ).respond_with_json(DUMMY_ACCOUNT_PAYLOAD)

        assert client.trading.account.get() == DUMMY_ACCOUNT_RESPONSE


class TestEditAccountApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.update(address_street="new street")

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/account",
            "method": "PUT",
            "json": {
                "address_street": "new street",
                "address_street_number": None,
                "address_city": None,
                "address_postal_code": None,
                "address_country": None,
            },
        }

    def test_get_account(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account",
            method="PUT",
            json={
                "address_street": "new street",
                "address_street_number": None,
                "address_city": None,
                "address_postal_code": None,
                "address_country": None,
            },
        ).respond_with_json(DUMMY_ACCOUNT_PAYLOAD)
        assert (
            client.trading.account.update(address_street="new street")
            == DUMMY_ACCOUNT_RESPONSE
        )


class TestGetWithdrawalsApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get_withdrawals()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account/withdrawals", "method": "GET"}

    def test_get_withdrawals(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account/withdrawals",
            method="GET",
        ).respond_with_json(DUMMY_WITHDRAWLS_PAYLOAD)
        assert client.trading.account.get_withdrawals() == DUMMY_WITHDRAWLS_RESPONSE

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account/withdrawals",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/account/withdrawals",
            method="GET",
        ).respond_with_json(DUMMY_WITHDRAWLS_PAYLOAD)

        assert client.trading.account.get_withdrawals() == DUMMY_WITHDRAWLS_RESPONSE


class TestWithdrawApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.withdraw(amount=100, pin="1234")

    @pytest.fixture
    def api_call_kwargs(self):
        return {
            "uri": "/account/withdrawals",
            "method": "POST",
            "json": {"amount": 100, "pin": "1234", "idempotency": None},
        }

    def test_get_withdrawals(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account/withdrawals",
            method="POST",
            json={"amount": 100, "pin": "1234", "idempotency": None},
        ).respond_with_json(DUMMY_WITHDRAW_PAYLOAD)
        assert (
            client.trading.account.withdraw(amount=100, pin="1234")
            == DUMMY_WITHDRAW_RESPONSE
        )


class TestGetBankStatementsApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get_bank_statements()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account/bankstatements", "method": "GET"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"type": "pay_in"}, "type=pay_in"),
            ({"from_": "beginning"}, "from=beginning"),
            ({"to": date(year=2000, month=3, day=3)}, "to=2000-03-03"),
            ({"sorting": "asc"}, "sorting=asc"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "type": "pay_in",
                    "from_": "beginning",
                    "to": date(year=2000, month=3, day=3),
                    "sorting": "asc",
                    "limit": 100,
                    "page": 7,
                },
                "type=pay_in&from=beginning&to=2000-03-03&sorting=asc&limit=100&page=7",
            ),
        ],
    )
    def test_get_bank_statements(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/account/bankstatements", query_string=query_string, method="GET"
        ).respond_with_json(DUMMY_BANK_STATEMENTS_PAYLOAD)
        assert (
            client.trading.account.get_bank_statements(**function_kwargs)
            == DUMMY_BANKSTATEMENTS_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account/bankstatements",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/account/bankstatements",
            method="GET",
        ).respond_with_json(DUMMY_BANK_STATEMENTS_PAYLOAD)

        assert (
            client.trading.account.get_bank_statements()
            == DUMMY_BANKSTATEMENTS_RESPONSE
        )


class TestGetDocumentsApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get_documents()

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account/documents", "method": "GET"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"sorting": "asc"}, "sorting=asc"),
            ({"limit": 100}, "limit=100"),
            ({"page": 7}, "page=7"),
            (
                {
                    "sorting": "asc",
                    "limit": 100,
                    "page": 7,
                },
                "sorting=asc&limit=100&page=7",
            ),
        ],
    )
    def test_get_documents(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/account/documents", query_string=query_string, method="GET"
        ).respond_with_json(DUMMY_GET_DOCUMENTS_PAYLOAD)
        assert (
            client.trading.account.get_documents(**function_kwargs)
            == DUMMY_GET_DOCUMENTS_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account/documents",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/account/documents",
            method="GET",
        ).respond_with_json(DUMMY_GET_DOCUMENTS_PAYLOAD)

        assert client.trading.account.get_documents() == DUMMY_GET_DOCUMENTS_RESPONSE


class TestGetDocumentApi(CommonTradingApiTests):
    def make_api_call(self, client: Api):
        return client.trading.account.get_document("foo")

    @pytest.fixture
    def api_call_kwargs(self):
        return {"uri": "/account/documents/foo", "method": "GET"}

    @pytest.mark.parametrize(
        "function_kwargs,query_string",
        [
            ({}, ""),
            ({"no_redirect": False}, "no_redirect=False"),
        ],
    )
    def test_get_document(
        self, client: Api, httpserver: HTTPServer, function_kwargs, query_string
    ):
        httpserver.expect_oneshot_request(
            "/account/documents/foo", query_string=query_string, method="GET"
        ).respond_with_json(DUMMY_GET_DOCUMENT_PAYLOAD)
        assert (
            client.trading.account.get_document("foo", **function_kwargs)
            == DUMMY_GET_DOCUMENT_RESPONSE
        )

    def test_retry_on_error(self, client: Api, httpserver: HTTPServer):
        httpserver.expect_oneshot_request(
            "/account/documents/foo",
            method="GET",
        ).respond_with_data(status=500)

        httpserver.expect_oneshot_request(
            "/account/documents/foo",
            method="GET",
        ).respond_with_json(DUMMY_GET_DOCUMENT_PAYLOAD)

        assert client.trading.account.get_document("foo") == DUMMY_GET_DOCUMENT_RESPONSE

    def test_raise_on_invalid_input(self, client: Api):
        with pytest.raises(ValueError):
            client.trading.account.get_document("")
