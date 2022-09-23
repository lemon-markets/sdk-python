import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time, timezone
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Tuple,
    Type,
    TypeVar,
    Union, Optional,
)

from typing_extensions import Literal

from lemon.errors import APIError

Sorting = Literal["asc", "desc"]
Environment = Literal["paper", "money"]
Days = int


class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        return super().default(o)


def filter_out_optionals(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def convert_datetime(value: Union[str, int]) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except:
        try:
            return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
        except Exception as exc:
            raise APIError(exc) from exc


BASIC_PARSERS = {
    datetime: convert_datetime,
    date: lambda value: datetime.fromisoformat(value).date(),
}


def _make_parser(type_: Type[Any]) -> Callable[[Any], Any]:
    # check if given type is from typing module
    origin = getattr(type_, "__origin__", None)

    if origin is None:
        # base type or regular type or class derived from BaseModel
        if issubclass(type_, BaseModel):
            return type_._from_data
        parser = BASIC_PARSERS.get(type_)
        if parser is not None:
            return parser
        return type_

    # typing.List[X]
    if origin is list:
        # extract X
        type_ = type_.__args__[0]
        parser = _make_parser(type_)
        return lambda val: [parser(item) for item in val]  # type: ignore

    # typing.Optional[X]
    if origin is Union:
        # extract X
        l, r = type_.__args__
        type_ = l if l is not None else r
        return _make_parser(type_)

    if origin is Literal:
        # we do not parse the content of literal
        return str

    raise ValueError(f"Unsupported type {type_}")


class BaseModelMeta(type):
    def __new__(
            cls, name: str, bases: Tuple[Any], dct: Dict[str, Any]
    ) -> "BaseModelMeta":
        if "__annotations__" not in dct:
            return super().__new__(cls, name, bases, dct)

        annotations = dct["__annotations__"]
        dct["_parsers"] = {
            key: _make_parser(type_)
            for key, type_ in annotations.items()
            if not key.startswith("_")
        }
        dct["__slots__"] = tuple(annotations.keys())

        return super().__new__(cls, name, bases, dct)


TBaseModel = TypeVar("TBaseModel", bound="BaseModel")


class BaseModel(metaclass=BaseModelMeta):
    __slots__ = tuple()  # type: ignore

    def dict(self) -> Dict[str, Any]:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(asdict(self), cls=JSONEncoder)

    @classmethod
    def _from_data(cls: Type[TBaseModel], data: Dict[str, Any]) -> TBaseModel:
        kwargs = {}

        for key, parser in cls._parsers.items():  # type: ignore # pylint: disable=E1101
            val = data.get(key)
            kwargs[key] = parser(val) if val is not None else None

        return cls(**kwargs)


@dataclass
class IterableResponseBase(BaseModel):
    next: Optional[str]
    _client: Optional["Client"]

    @classmethod
    def _from_data(
            cls: Type[TBaseModel], data: Dict[str, Any], client: "Client"
    ) -> TBaseModel:
        kwargs = {}

        for key, parser in cls._parsers.items():  # type: ignore # pylint: disable=E1101
            val = data.get(key)
            kwargs[key] = parser(val) if val is not None else None

        return cls(**kwargs, next=data.get("next"), _client=client)

    def auto_iter(self) -> Iterator:
        data = self
        while True:
            for el in data.results:
                yield el

            if not data.next:
                break

            data = self._from_data(
                self._client.get(data.next).json(), client=self._client
            )
