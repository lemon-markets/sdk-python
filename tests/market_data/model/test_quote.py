from datetime import datetime

from lemon.market_data.model import GetQuotesResponse, Quote

RESPONSE = GetQuotesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Quote(
            isin="US88160R1014",
            b_v=87,
            a_v=87,
            b=921,
            a=921,
            t=datetime.fromisoformat("2021-10-28T08:51:03.669+00:00"),
            mic="XMUN",
        )
    ],
    total=1,
    page=1,
    pages=1,
)

DICT_RESPONSE = {
    "time": datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    "results": [
        {
            "isin": "US88160R1014",
            "b_v": 87,
            "a_v": 87,
            "b": 921,
            "a": 921,
            "t": datetime.fromisoformat("2021-10-28T08:51:03.669+00:00"),
            "mic": "XMUN",
        }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
}


def test_get_quotes_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
