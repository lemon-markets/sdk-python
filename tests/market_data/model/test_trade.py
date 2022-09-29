from datetime import datetime

from lemon.market_data.model import GetTradesResponse, Trade

RESPONSE = GetTradesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Trade(
            isin="US19260Q1076",
            p=274,
            pbv=35,
            v=2,
            t=datetime.fromisoformat("2021-10-28T09:05:14.474+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
    next=None,
    _client=None,
)

DICT_RESPONSE = {
    "time": datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    "results": [
        {
            "isin": "US19260Q1076",
            "p": 274,
            "pbv": 35,
            "v": 2,
            "t": datetime.fromisoformat("2021-10-28T09:05:14.474+00:00"),
            "mic": "XMUN",
        }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "_client": None,
    "next": None,
}


def test_get_trades_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
