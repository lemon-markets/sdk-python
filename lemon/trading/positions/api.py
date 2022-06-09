from datetime import datetime
from typing import Optional

from lemon.helpers import ApiClient, Sorting
from lemon.trading.positions.models import (
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
            "/v1/positions",
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
        type: Optional[StatementType] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetStatementsResponse:
        resp = self._client.get(
            "/v1/positions/statements",
            params={
                "isin": isin,
                "from": from_,
                "to": to,
                "type": type,
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
            "/v1/positions/performance",
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
