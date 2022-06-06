from typing import List, Optional

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.venues.models import GetVenuesResponse


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
            "/venues",
            params={
                "mic": mic,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetVenuesResponse._from_data(resp.json())
