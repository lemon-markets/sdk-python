import json
from dataclasses import asdict
from datetime import date, datetime, time
from typing import Any, Callable, Dict

from typing_extensions import Literal

Sorting = Literal["asc", "desc"]
Environment = Literal["paper", "money"]
Days = int


def to_type(type_: Callable[[Any], Any], value: Any) -> Any:
    return type_(value) if value is not None else None


def to_date(x: str) -> date:
    return datetime.fromisoformat(x).date()


class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        return super().default(o)


class BaseModel:
    def dict(self) -> Dict[str, Any]:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(asdict(self), cls=JSONEncoder)
