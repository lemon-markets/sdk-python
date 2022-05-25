from typing import List, Literal, Optional

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.ohlc.models import GetOhlcResponse


class Ohlc:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        x1: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetOhlcResponse:
        resp = self._client.get(
            f"/ohlc/{x1}",
            query_params={
                "mic": mic,
                "isin": isin,
                "from": from_,
                "to": to,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetOhlcResponse._from_data(resp.json())
