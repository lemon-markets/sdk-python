from typing import List, Optional

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.instruments.models import GetInstrumentsResponse


class Instruments:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        isin: Optional[List[str]] = None,
        search: Optional[str] = None,
        type: Optional[List[str]] = None,
        mic: Optional[List[str]] = None,
        currency: Optional[str] = None,
        tradable: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetInstrumentsResponse:
        resp = self._client.get(
            "/instruments",
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
