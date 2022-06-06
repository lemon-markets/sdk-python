from typing import List, Optional

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.quotes.models import GetQuotesResponse


class Quotes:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[str] = None,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetQuotesResponse:
        resp = self._client.get(
            "/quotes/latest",
            params={
                "isin": isin,
                "mic": mic,
                "from": from_,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetQuotesResponse._from_data(resp.json())
