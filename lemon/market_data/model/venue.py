from dataclasses import dataclass
from datetime import date, datetime, time, tzinfo
from typing import Dict, List

import pytz

from lemon.types import BaseModel


def _build_time(time: str, timezone: tzinfo) -> time:
    return datetime.strptime(time, "%H:%M").time().replace(tzinfo=timezone)


@dataclass
class OpeningHours(BaseModel):
    start: time
    end: time

    @staticmethod
    def _from_data(data: Dict[str, str]) -> "OpeningHours":
        timezone = pytz.timezone(data["timezone"])
        return OpeningHours(
            start=_build_time(data["start"], timezone),
            end=_build_time(data["end"], timezone),
        )


@dataclass
class Venue(BaseModel):
    name: str
    title: str
    mic: str
    is_open: bool
    opening_hours: OpeningHours
    opening_days: List[date]


@dataclass
class GetVenuesResponse(BaseModel):
    time: datetime
    results: List[Venue]
    total: int
    page: int
    pages: int
