from datetime import datetime

from lemon.market_data.model import GetInstrumentsResponse, Instrument, InstrumentVenue

RESPONSE = GetInstrumentsResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Instrument(
            isin="US19260Q1076",
            wkn="A2QP7J",
            name="COINBASE GLB.CL.A -,00001",
            title="COINBASE GLOBAL INC",
            symbol="1QZ",
            type="stock",
            venues=[
                InstrumentVenue(
                    name="Börse München - Gettex",
                    title="Gettex",
                    mic="XMUN",
                    is_open=True,
                    tradable=True,
                    currency="EUR",
                )
            ],
        )
    ],
    total=26283,
    page=2,
    pages=263,
    next=None,
    _client=None,
    _headers=None,
)

DICT_RESPONSE = {
    "time": datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    "results": [
        {
            "isin": "US19260Q1076",
            "wkn": "A2QP7J",
            "name": "COINBASE GLB.CL.A -,00001",
            "title": "COINBASE GLOBAL INC",
            "symbol": "1QZ",
            "type": "stock",
            "venues": [
                {
                    "name": "Börse München - Gettex",
                    "title": "Gettex",
                    "mic": "XMUN",
                    "is_open": True,
                    "tradable": True,
                    "currency": "EUR",
                }
            ],
        }
    ],
    "total": 26283,
    "page": 2,
    "pages": 263,
    "_client": None,
    "_headers": None,
    "next": None,
}


def test_get_instruments_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
