from datetime import datetime
from typing import List, Optional

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.trades.models import GetTradesResponse


class Trades:
    def __init__(self, client: ApiClient):
        self._client = client

    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetTradesResponse:
        resp = self._client.get(
            "/v1/trades/latest",
            params={
                "mic": mic,
                "isin": isin,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetTradesResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
        )
