from typing import List, Optional

from lemon.helpers import ApiClient, Sorting, handle_market_data_errors
from lemon.market_data.model import GetVenuesResponse


class Venues:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        mic: Optional[List[str]] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetVenuesResponse:
        resp = self._client.get(
            "venues",
            params={
                "mic": mic,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        if not resp.ok:
            handle_market_data_errors(resp.json())
        return GetVenuesResponse._from_data(resp.json())
