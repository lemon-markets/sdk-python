from datetime import datetime
from typing import List, Literal, Optional, Union

from lemon.helpers import ApiClient, Days, Sorting
from lemon.market_data.ohlc.models import GetOhlcResponse


class Ohlc:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Union[datetime, Literal["latest"], None] = None,
        to: Union[datetime, Days, None] = None,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetOhlcResponse:
        resp = self._client.get(
            f"ohlc/{period}",
            params={
                "mic": mic,
                "isin": isin,
                "from": from_,
                "to": f"P{to}D" if isinstance(to, Days) else to,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetOhlcResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
        )
