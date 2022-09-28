from datetime import date, datetime

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

GET_ACCOUNT_RESPONSE = GetAccountResponse(
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

DICT_GET_ACCOUNT_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-22T15:37:56.520+00:00"),
    "mode": "paper",
    "results": {
        "created_at": datetime.fromisoformat("2021-10-12T10:29:49.769+00:00"),
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
        "approved_at": datetime.fromisoformat("2021-11-19T07:40:12.563+00:00"),
        "trading_plan": "investor",
        "data_plan": "investor",
        "tax_allowance": 8010000,
        "tax_allowance_start": date(year=2021, month=1, day=1),
        "tax_allowance_end": date(year=2021, month=1, day=1),
    },
}

GET_WITHDRAWLS_RESPONSE = GetWithdrawalsResponse(
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

DICT_GET_WITHDRAWLS_RESPONSE = {
    "time": datetime.fromisoformat("2021-12-15T11:21:21.023+00:00"),
    "mode": "paper",
    "results": [
        {
            "id": "wtd_pyQTPbbLLMNBQTM0mzkK7Ygb8kH60Ff10X",
            "amount": 1000000,
            "created_at": datetime.fromisoformat("2021-12-15T11:21:05.853+00:00"),
            "date": datetime.fromisoformat("2021-12-15T23:12:02.765+00:00").date(),
            "idempotency": "1234abcd",
        },
    ],
    "total": 80,
    "page": 2,
    "pages": 4,
}

GET_WITHDRAW_RESPONSE = WithdrawResponse(
    time=datetime.fromisoformat("2021-11-22T15:37:56.520+00:00"),
    mode="paper",
)

DICT_GET_WITHDRAW_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-22T15:37:56.520+00:00"),
    "mode": "paper",
}

GET_BANK_STATEMENTS_RESPONSE = GetBankStatementsResponse(
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
    _client=None,
    next=None
)

DICT_GET_BANK_STATEMENTS_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-22T15:41:04.028+00:00"),
    "mode": "paper",
    "results": [
        {
            "id": "bst_pyQKKTTSS0Q2drg2J7yRhTwBkMPd1JgZzZ",
            "account_id": "acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
            "type": "order_buy",
            "date": date(year=2021, month=12, day=16),
            "amount": 100000,
            "quantity": 10,
            "isin": "US19260Q1076",
            "isin_title": "COINBASE GLOBAL INC.",
            "created_at": datetime.fromisoformat("2021-12-17T01:37:03.362+00:00"),
        },
    ],
    "total": 80,
    "page": 2,
    "pages": 4,
    "_client": None,
    "next": None
}

GET_DOCUMENTS_RESPONSE = GetDocumentsResponse(
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

DICT_GET_DOCUMENTS_RESPONSE = {
    "time": datetime.fromisoformat("2021-11-22T15:41:04.028+00:00"),
    "mode": "paper",
    "results": [
        {
            "id": "doc_pyNjNcc77ht3T3lH8dJa5fD8jhj2JHJ1xX",
            "name": "account_opening.pdf",
            "created_at": datetime.fromisoformat("2021-10-19T14:58:52.813"),
            "category": "kyc",
            "link": "lemon.markets/v1/account/documents/doc_pyNjNcc77ht3T3lH8dJa5fD8jhj2JHJ1xX",
            "viewed_first_at": datetime.fromisoformat("2021-10-19T14:58:52.813"),
            "viewed_last_at": datetime.fromisoformat("2021-10-19T14:58:52.813"),
        },
    ],
    "total": 80,
    "page": 2,
    "pages": 4,
}

GET_DOCUMENT_RESPONSE = GetDocumentResponse(
    time=datetime.fromisoformat("2022-05-30T09:47:16.769"),
    mode="paper",
    results=DocumentUrl(public_url="foo"),
)

DICT_GET_DOCUMENT_RESPONSE = {
    "time": datetime.fromisoformat("2022-05-30T09:47:16.769"),
    "mode": "paper",
    "results": {"public_url": "foo"},
}


def test_get_account_response_is_serializable():
    assert GET_ACCOUNT_RESPONSE.dict() == DICT_GET_ACCOUNT_RESPONSE
    assert GET_ACCOUNT_RESPONSE.json()


def test_get_withdrawls_response_is_serializable():
    assert GET_WITHDRAWLS_RESPONSE.dict() == DICT_GET_WITHDRAWLS_RESPONSE
    assert GET_WITHDRAWLS_RESPONSE.json()


def test_get_withdrawl_response_is_serializable():
    assert GET_WITHDRAW_RESPONSE.dict() == DICT_GET_WITHDRAW_RESPONSE
    assert GET_WITHDRAW_RESPONSE.json()


def test_get_bank_statements_response_is_serializable():
    assert GET_BANK_STATEMENTS_RESPONSE.dict() == DICT_GET_BANK_STATEMENTS_RESPONSE
    assert GET_BANK_STATEMENTS_RESPONSE.json()


def test_get_documents_response_is_serializable():
    assert GET_DOCUMENTS_RESPONSE.dict() == DICT_GET_DOCUMENTS_RESPONSE
    assert GET_DOCUMENTS_RESPONSE.json()


def test_get_document_response_is_serializable():
    assert GET_DOCUMENT_RESPONSE.dict() == DICT_GET_DOCUMENT_RESPONSE
    assert GET_DOCUMENT_RESPONSE.json()
