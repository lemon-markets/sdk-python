from datetime import datetime
from typing import List, Optional, Union

from typing_extensions import Literal

from lemon.base import Client
from lemon.market_data.model import GetQuotesResponse
from lemon.types import Days, Sorting


class Quotes:
    def __init__(self, client: Client):
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
        return GetQuotesResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
            client=self._client,
        )

    def get(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Optional[Union[datetime, Days]] = None,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ):
        resp = self._client.get(
            "quotes",
            params={
                "isin": isin,
                "mic": mic,
                "from": from_,
                "to": f"P{to}D" if isinstance(to, Days) else to,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetQuotesResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
            client=self._client,
        )
