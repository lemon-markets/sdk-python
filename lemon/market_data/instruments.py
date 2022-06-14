from typing import List, Optional

from lemon.base import Client
from lemon.market_data.model import GetInstrumentsResponse, InstrumentType
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
