from datetime import datetime

from lemon.streaming.model import Token

RESPONSE = Token(
    token="token123",
    user_id="user_123",
    expires_at=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
)

DICT_RESPONSE = {
    "token": "token123",
    "user_id": "user_123",
    "expires_at": datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
}


def test_authenticate_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
