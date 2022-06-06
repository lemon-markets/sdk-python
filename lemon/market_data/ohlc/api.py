from datetime import datetime
from typing import List, Literal, Optional, Union, overload

from lemon.helpers import ApiClient, Sorting
from lemon.market_data.ohlc.models import DayOffset, GetOhlcResponse


class Ohlc:
    def __init__(self, client: ApiClient):
        self._client = client

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[True],
    ) -> GetOhlcResponse[float, int]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[False],
    ) -> GetOhlcResponse[float, datetime]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[None] = None,
    ) -> GetOhlcResponse[float, datetime]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[True],
    ) -> GetOhlcResponse[int, int]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[False],
    ) -> GetOhlcResponse[int, datetime]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[None] = None,
    ) -> GetOhlcResponse[int, datetime]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[True],
    ) -> GetOhlcResponse[int, int]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[False],
    ) -> GetOhlcResponse[int, datetime]:
        ...

    @overload
    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[None] = None,
    ) -> GetOhlcResponse[int, datetime]:
        ...

    def get(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Union[datetime, DayOffset, None] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
    ) -> Union[
        GetOhlcResponse[int, int],
        GetOhlcResponse[int, datetime],
        GetOhlcResponse[float, int],
        GetOhlcResponse[float, datetime],
    ]:
        resp = self._client.get(
            f"/ohlc/{period}",
            params={
                "mic": mic,
                "isin": isin,
                "from": from_,
                "to": f"P{to}D" if isinstance(to, DayOffset) else to,
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

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[True],
    ) -> GetOhlcResponse[float, int]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[False],
    ) -> GetOhlcResponse[float, datetime]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[True],
        epoch: Literal[None] = None,
    ) -> GetOhlcResponse[float, datetime]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[True],
    ) -> GetOhlcResponse[int, int]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[False],
    ) -> GetOhlcResponse[int, datetime]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[False],
        epoch: Literal[None] = None,
    ) -> GetOhlcResponse[int, datetime]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[True],
    ) -> GetOhlcResponse[int, int]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[False],
    ) -> GetOhlcResponse[int, datetime]:
        ...

    @overload
    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Literal[None] = None,
        epoch: Literal[None] = None,
    ) -> GetOhlcResponse[int, datetime]:
        ...

    def get_latest(
        self,
        period: Literal["m1", "h1", "d1"],
        isin: List[str],
        mic: Optional[str] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        *,
        decimals: Optional[bool] = None,
        epoch: Optional[bool] = None,
    ) -> Union[
        GetOhlcResponse[int, int],
        GetOhlcResponse[int, datetime],
        GetOhlcResponse[float, int],
        GetOhlcResponse[float, datetime],
    ]:
        resp = self._client.get(
            f"/ohlc/{period}/latest",
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
        return GetOhlcResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
        )
