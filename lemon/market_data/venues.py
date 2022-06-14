from typing import List, Optional

from lemon.base import Client
from lemon.market_data.model import GetVenuesResponse
from lemon.types import Sorting


class Venues:
    def __init__(self, client: Client):
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
        return GetVenuesResponse._from_data(resp.json())
