from typing import List, Optional

from lemon.helpers import ApiClient, Sorting, encode_query_string
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
        query_params = encode_query_string(
            isin=isin,
            search=search,
            type=type,
            mic=mic,
            currency=currency,
            tradable=tradable,
            sorting=sorting,
            limit=limit,
            page=page,
        )
        resp = self._client.get(f"/instruments?{query_params}")
        return GetInstrumentsResponse._from_data(resp.json())
