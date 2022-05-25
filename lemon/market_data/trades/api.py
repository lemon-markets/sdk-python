from typing import List, Optional

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.trades.models import GetTradesResponse


class Trades:
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
    ) -> GetTradesResponse:
        resp = self._client.get(
            "/trades/latest",
            query_params={
                "mic": mic,
                "isin": isin,
                "from": from_,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetTradesResponse._from_data(resp.json())
