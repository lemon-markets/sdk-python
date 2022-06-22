from datetime import datetime
from typing import List, Optional

from lemon.base import Client
from lemon.trading.model import (
    GetPerformanceResponse,
    GetPositionsResponse,
    GetStatementsResponse,
    StatementType,
)
from lemon.types import Sorting


class Positions:
    def __init__(self, client: Client):
        self._client = client

    def get(
        self,
        isin: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetPositionsResponse:
        resp = self._client.get(
            "positions",
            params={
                "isin": isin,
                "limit": limit,
                "page": page,
            },
        )
        return GetPositionsResponse._from_data(resp.json())

    def get_statements(
        self,
        isin: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        types: Optional[List[StatementType]] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetStatementsResponse:
        resp = self._client.get(
            "positions/statements",
            params={
                "isin": isin,
                "from": from_,
                "to": to,
                "types": types,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetStatementsResponse._from_data(resp.json())

    def get_performance(
        self,
        isin: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetPerformanceResponse:
        resp = self._client.get(
            "positions/performance",
            params={
                "isin": isin,
                "from": from_,
                "to": to,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
        )
        return GetPerformanceResponse._from_data(resp.json())
