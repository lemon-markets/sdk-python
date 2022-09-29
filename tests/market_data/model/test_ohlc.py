from datetime import datetime

from lemon.market_data.model import GetOhlcResponse, OhlcData

RESPONSE = GetOhlcResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        OhlcData(
            isin="US88160R1014",
            o=777,
            h=777,
            l=762,
            c=768,
            v=433,
            pbv=333645,
            t=datetime.fromisoformat("2021-09-02T00:00:00.000+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
    _client=None,
    next=None,
)

DICT_RESPONSE = {
    "time": datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    "results": [
        {
            "isin": "US88160R1014",
            "o": 777,
            "h": 777,
            "l": 762,
            "c": 768,
            "v": 433,
            "pbv": 333645,
            "t": datetime.fromisoformat("2021-09-02T00:00:00.000+00:00"),
            "mic": "XMUN",
        }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "_client": None,
    "next": None,
}


def test_get_ohlc_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
