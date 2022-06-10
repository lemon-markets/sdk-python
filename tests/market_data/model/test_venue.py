from datetime import date, datetime, time

import pytz

from lemon.market_data.model import GetVenuesResponse, OpeningHours, Venue

RESPONSE = GetVenuesResponse(
    time=datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    results=[
        Venue(
            name="Börse München - Gettex",
            title="Gettex",
            mic="XMUN",
            is_open=True,
            opening_hours=OpeningHours(
                start=time(
                    hour=8,
                    minute=0,
                    tzinfo=pytz.timezone("Europe/Berlin"),
                ),
                end=time(
                    hour=22,
                    minute=0,
                    tzinfo=pytz.timezone("Europe/Berlin"),
                ),
            ),
            opening_days=[
                date(year=2021, month=12, day=6),
            ],
        )
    ],
    total=3,
    page=2,
    pages=3,
)

DICT_RESPONSE = {
    "time": datetime.fromisoformat("2022-02-14T20:44:03.759+00:00"),
    "results": [
        {
            "name": "Börse München - Gettex",
            "title": "Gettex",
            "mic": "XMUN",
            "is_open": True,
            "opening_hours": {
                "start": time(
                    hour=8,
                    minute=0,
                    tzinfo=pytz.timezone("Europe/Berlin"),
                ),
                "end": time(
                    hour=22,
                    minute=0,
                    tzinfo=pytz.timezone("Europe/Berlin"),
                ),
            },
            "opening_days": [date(year=2021, month=12, day=6)],
        }
    ],
    "total": 3,
    "page": 2,
    "pages": 3,
}


def test_get_venues_response_is_serializable():
    assert RESPONSE.dict() == DICT_RESPONSE
    assert RESPONSE.json()
