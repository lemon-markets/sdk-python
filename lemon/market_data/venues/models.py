from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Dict, List, cast

import pytz


def _build_time(time: str, timedelta: timedelta) -> time:
    return (
        datetime.strptime(time, "%H:%M")
        .time()
        .replace(tzinfo=timezone(offset=timedelta))
    )


@dataclass
class OpeningHours:
    start: time
    end: time

    @staticmethod
    def _from_data(data: Dict[str, str]) -> "OpeningHours":
        timezone = cast(
            timedelta, datetime.now(pytz.timezone(data["timezone"])).utcoffset()
        )
        return OpeningHours(
            start=_build_time(data["start"], timezone),
            end=_build_time(data["end"], timezone),
        )


@dataclass
class Venue:
    name: str
    title: str
    mic: str
    is_open: bool
    opening_hours: OpeningHours
    opening_days: List[date]

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Venue":
        return Venue(
            name=data["name"],
            title=data["title"],
            mic=data["mic"],
            is_open=data["is_open"],
            opening_hours=OpeningHours._from_data(data["opening_hours"]),
            opening_days=[
                datetime.fromisoformat(opening_day).date()
                for opening_day in data["opening_days"]
            ],
        )


@dataclass
class GetVenuesResponse:
    time: datetime
    result: List[Venue]
    total: int
    page: int
    pages: int

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "GetVenuesResponse":
        return GetVenuesResponse(
            time=datetime.fromisoformat(data["time"]),
            result=[Venue._from_data(entry) for entry in data["results"]],
            total=int(data["total"]),
            page=int(data["page"]),
            pages=int(data["pages"]),
        )
