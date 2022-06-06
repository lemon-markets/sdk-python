from datetime import datetime
from typing import List, Literal, Optional, Union, overload

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.quotes.models import GetQuotesResponse


class Quotes:
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
    ) -> GetQuotesResponse[float, int]:
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
    ) -> GetQuotesResponse[float, datetime]:
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
    ) -> GetQuotesResponse[float, datetime]:
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
    ) -> GetQuotesResponse[int, int]:
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
    ) -> GetQuotesResponse[int, datetime]:
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
    ) -> GetQuotesResponse[int, datetime]:
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
    ) -> GetQuotesResponse[int, int]:
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
    ) -> GetQuotesResponse[int, datetime]:
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
    ) -> GetQuotesResponse[int, datetime]:
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
        GetQuotesResponse[int, int],
        GetQuotesResponse[int, datetime],
        GetQuotesResponse[float, int],
        GetQuotesResponse[float, datetime],
    ]:
        resp = self._client.get(
            "/quotes/latest",
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
        )
