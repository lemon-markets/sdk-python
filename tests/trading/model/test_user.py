from datetime import date, datetime

from lemon.trading.model import GetUserResponse, User

RESPONSE = GetUserResponse(
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

DICT_RESPONSE = {
    "time": datetime.fromisoformat("2022-06-01T18:37:03.817"),
    "mode": "paper",
    "results": {
        "created_at": datetime.fromisoformat("2022-06-01T18:37:03.817"),
        "user_id": "string",
        "firstname": "string",
        "lastname": "string",
        "email": "string",
        "phone": "string",
        "phone_verified": datetime.fromisoformat("2022-06-01T18:37:03.817"),
        "pin_verified": True,
        "account_id": "string",
        "trading_plan": "string",
        "data_plan": "string",
        "tax_allowance": 0,
        "tax_allowance_start": date(year=2022, month=6, day=1),
        "tax_allowance_end": date(year=2022, month=6, day=1),
        "optin_order_push": True,
        "optin_order_email": True,
        "country": "string",
        "language": "string",
        "timezone": "string",
    },
}


def test_get_user_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
