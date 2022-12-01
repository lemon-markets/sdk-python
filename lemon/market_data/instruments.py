from datetime import datetime, timezone
from http import HTTPStatus
from typing import List, Optional

from lemon.base import Client
from lemon.market_data.model import GetInstrumentsResponse, InstrumentType
from lemon.types import Sorting


class Instruments:
    def __init__(self, client: Client):
        self._client = client

    def get(
        self,
        isin: Optional[List[str]] = None,
        search: Optional[str] = None,
        type: Optional[List[InstrumentType]] = None,
        mic: Optional[List[str]] = None,
        currency: Optional[List[str]] = None,
        tradable: Optional[bool] = None,
        sorting: Optional[Sorting] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        modified_since: Optional[datetime] = None,
    ) -> GetInstrumentsResponse:
        headers = None
        if modified_since:
            headers = {}
            modified_since = modified_since.astimezone(timezone.utc)
            headers["if-modified-since"] = datetime.strftime(
                modified_since, "%a, %d %b %Y %H:%M:%S GMT"
            )
        resp = self._client.get(
            "instruments",
            params={
                "isin": isin,
                "search": search,
                "type": type,
                "mic": mic,
                "currency": currency,
                "tradable": tradable,
                "sorting": sorting,
                "limit": limit,
                "page": page,
            },
            headers=headers,
        )
        if resp.status_code == HTTPStatus.NOT_MODIFIED:
            data = {
                "status": "ok",
                "time": datetime.now(tz=timezone.utc).isoformat(
                    timespec="milliseconds"
                ),
                "results": [],
                "previous": None,
                "next": None,
                "total": 0,
                "page": 0,
                "pages": 0,
            }
        else:
            data = resp.json()
        return GetInstrumentsResponse._from_data(
            dict(data, _client=self._client, _headers=headers)
        )
