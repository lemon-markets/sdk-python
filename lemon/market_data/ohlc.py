from datetime import datetime
from typing import Iterator, List, Optional, Union

from typing_extensions import Literal

from lemon.base import Client
from lemon.market_data.model import GetOhlcResponse, OhlcData
from lemon.types import Days, Sorting


class Ohlc:
    def __init__(self, client: Client):
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
        period = period.strip().lower()  # type: ignore
        if not period:
            raise ValueError("Invalid period value")

        resp = self._client.get(
            f"ohlc/{period}",
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
        return GetOhlcResponse._from_data(
            data=resp.json(),
            t_type=float if decimals else int,
            k_type=int if epoch else datetime.fromisoformat,  # type: ignore
        )

    def iter(
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
    ) -> Iterator[OhlcData]:
        period = period.strip().lower()  # type: ignore
        if not period:
            raise ValueError("Invalid period value")

        resp = self._client.get(
            f"ohlc/{period}",
            params={
                "isin": isin,
                "mic": mic,
                "from": from_,
                "to": f"P{to}D" if isinstance(to, Days) else to,
                "decimals": decimals,
                "epoch": epoch,
                "sorting": sorting,
                "limit": limit,
            },
        )
        while True:
            resp_data = resp.json()
            for result in resp_data["results"]:
                yield OhlcData._from_data(
                    result,
                    t_type=float if decimals else int,
                    k_type=int if epoch else datetime.fromisoformat,
                )  # type: ignore)
            if resp_data["next"]:
                resp = self._client.get(resp_data["next"])
            else:
                break
