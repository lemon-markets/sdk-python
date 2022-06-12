from datetime import datetime
from typing import List, Optional

from lemon.helpers import ApiClient, Sorting, handle_trading_errors
from lemon.trading.model import (
    GetPerformanceResponse,
    GetPositionsResponse,
    GetStatementsResponse,
    StatementType,
)


class Positions:
    def __init__(self, client: ApiClient):
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
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
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
        if not resp.ok:
            handle_trading_errors(resp.json())
        return GetPerformanceResponse._from_data(resp.json())
