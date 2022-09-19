from typing import Iterator, List, Optional

from lemon.base import Client
from lemon.market_data.model import GetInstrumentsResponse, InstrumentType, Instrument
from lemon.types import Sorting


class Instruments:
    def __init__(self, client: Client):
        self._client = client

    def get(
        self,
        isin: Optional[List[str]] = None,
        search: Optional[str] = None,
        type: Optional[List[InstrumentType]] = None,
        mic: Optional[List[str]] = None,
        currency: Optional[List[str]] = None,
        tradable: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetInstrumentsResponse:
        resp = self._client.get(
            "instruments",
            params={
                "isin": isin,
                "search": search,
                "type": type,
                "mic": mic,
                "currency": currency,
                "tradable": tradable,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetInstrumentsResponse._from_data(resp.json())

    def iter(
        self,
        isin: Optional[List[str]] = None,
        search: Optional[str] = None,
        type: Optional[List[InstrumentType]] = None,
        mic: Optional[List[str]] = None,
        currency: Optional[List[str]] = None,
        tradable: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Iterator[Instrument]:
        while True:
            resp = self._client.get(
                "instruments",
                params={
                    "isin": isin,
                    "search": search,
                    "type": type,
                    "mic": mic,
                    "currency": currency,
                    "tradable": tradable,
                    "sorting": sorting,
                    "limit": limit,
                    "page": page,
                },
            )
            for result in resp.json()["results"]:
                yield Instrument._from_data(result)
            if resp.json()["page"] == resp.json()["pages"]:
                break
            page = int(resp.json()["page"]) + 1