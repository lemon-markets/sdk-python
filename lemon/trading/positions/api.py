from typing import Optional

from lemon.helpers import ApiClient
from lemon.trading.positions.models import GetPositionsResponse


class Positions:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        isin: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetPositionsResponse:
        resp = self._client.get(
            "/positions",
            query_params={
                "isin": isin,
                "limit": limit,
                "page": page,
            },
        )
        return GetPositionsResponse._from_data(resp.json())
