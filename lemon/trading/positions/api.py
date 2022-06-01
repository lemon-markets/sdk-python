from datetime import datetime
from typing import Optional

from lemon.helpers import ApiClient, Sorting
from lemon.trading.positions.models import (
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
            "/positions",
            query_params={
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
            "/positions/statements",
            query_params={
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
