from datetime import datetime
from typing import List, Literal, Optional, Union, overload

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.trades.models import GetTradesResponse


class Trades:
    def __init__(self, client: ApiClient):
        self._client = client

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[True],
    ) -> GetTradesResponse[float, int]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[False],
    ) -> GetTradesResponse[float, datetime]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[None] = None,
    ) -> GetTradesResponse[float, datetime]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[True],
    ) -> GetTradesResponse[int, int]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[False],
    ) -> GetTradesResponse[int, datetime]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[None] = None,
    ) -> GetTradesResponse[int, datetime]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[True],
    ) -> GetTradesResponse[int, int]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[False],
    ) -> GetTradesResponse[int, datetime]:
        ...

    @overload
    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[None] = None,
    ) -> GetTradesResponse[int, datetime]:
        ...

    def get_latest(
        self,
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
    ) -> Union[
        GetTradesResponse[int, int],
        GetTradesResponse[int, datetime],
        GetTradesResponse[float, int],
        GetTradesResponse[float, datetime],
    ]:
        resp = self._client.get(
            "/trades/latest",
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
