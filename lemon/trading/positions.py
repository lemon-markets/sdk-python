from datetime import datetime
from typing import List, Optional

from lemon.base import Client
from lemon.trading.model import (
    GetPerformanceResponse,
    GetPositionsResponse,
    GetStatementsResponse,
    Performance, Position, Statement,
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

    def iter(
        self,
        isin: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> GetPositionsResponse:
        resp = self._client.get(
            "positions",
            params={
                "isin": isin,
                "limit": limit,
            },
        )
        while True:
            resp = resp.json()
            for result in resp["results"]:
                yield Position._from_data(result)
            if resp["next"]:
                resp = self._client.get(resp["next"])
            else:
                break
    
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

    def iter_statements(
        self,
        isin: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        types: Optional[List[StatementType]] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
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
            },
        )
        while True:
            resp = resp.json()
            for result in resp["results"]:
                yield Statement._from_data(result)
            if resp["next"]:
                resp = self._client.get(resp["next"])
            else:
                break


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

    def iter_performance(
        self,
        isin: Optional[str] = None,
        from_: Optional[datetime] = None,
        to: Optional[datetime] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
    ) -> GetPerformanceResponse:
        resp = self._client.get(
            "positions/performance",
            params={
                "isin": isin,
                "from": from_,
                "to": to,
                "sorting": sorting,
                "limit": limit,
            },
        )
        while True:
            resp = resp.json()
            for result in resp["results"]:
                yield Performance._from_data(result)
            if resp["next"]:
                resp = self._client.get(resp["next"])
            else:
                break
