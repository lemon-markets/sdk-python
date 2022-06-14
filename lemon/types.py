import json
from dataclasses import asdict
from datetime import date, datetime, time
from typing import Any, Dict, Type, TypeVar, Union

from typing_extensions import Literal

Sorting = Literal["asc", "desc"]
Environment = Literal["paper", "money"]
Days = int


BASIC_PARSERS = {
    datetime: datetime.fromisoformat,
    date: lambda value: datetime.fromisoformat(value).date(),
}


def _final_parse(type_: Type[Any], value: Any) -> Any:
    if issubclass(type_, BaseModel):
        return type_._from_data(value)
    parser = BASIC_PARSERS.get(type_)
    if parser is not None:
        return parser(value)  # type: ignore
    return type_(value)


def _unpack_by_origin(origin: Any, type_: Type[Any]) -> Type[Any]:
    if origin is Union:
        l, r = type_.__args__
        type_ = l if l is not None else r

    if origin is Literal:
        type_ = str

    origin = getattr(type_, "__origin__", None)
    if origin is None:
        return type_
    return _unpack_by_origin(origin, type_)


def _parse_as(type_: Type[Any], value: Any) -> Any:
    if value is None:
        return None

    origin = getattr(type_, "__origin__", None)
    if origin is list:
        type_ = type_.__args__[0]
        return [_parse_as(type_, item) for item in value]

    if origin is not None:
        type_ = _unpack_by_origin(origin, type_)

    return _final_parse(type_, value)


class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        return super().default(o)


TBaseModel = TypeVar("TBaseModel", bound="BaseModel")


class BaseModel:
    def dict(self) -> Dict[str, Any]:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(asdict(self), cls=JSONEncoder)

    @classmethod
    def _from_data(cls: Type[TBaseModel], data: Dict[str, Any]) -> TBaseModel:
        kwargs = {
            key: _parse_as(type_, data.get(key))
            for key, type_ in cls.__annotations__.items()  # pylint: disable=E1101
        }
        return cls(**kwargs)
