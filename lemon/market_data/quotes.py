from datetime import datetime
from typing import List, Optional

from lemon.helpers import ApiClient, Sorting, handle_market_data_errors
from lemon.market_data.model import GetQuotesResponse


class Quotes:
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
    ) -> GetQuotesResponse:
        resp = self._client.get(
            "quotes/latest",
            params={
                "isin": isin,
                "mic": mic,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        if not resp.ok:
            handle_market_data_errors(resp.json())
        return GetQuotesResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
        )
