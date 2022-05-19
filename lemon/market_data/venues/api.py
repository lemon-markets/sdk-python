from typing import Optional

from lemon.errors import UnexpectedError
from lemon.helpers import ApiClient, encode_query_string
from lemon.market_data.venues.errors import InvalidVenuesQuery
from lemon.market_data.venues.models import GetVenuesResponse


class Venues:
    def __init__(self, client: ApiClient):
        self._client = client

    def get(
        self,
        market_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> GetVenuesResponse:
        query_params = encode_query_string(market_id=market_id, limit=limit, page=page)

        resp = self._client.get(f"/venues?{query_params}")

        if resp.ok:
            return GetVenuesResponse._from_data(resp.json())

        error = resp.json()
        error_code = error["error_code"]
        if error_code == InvalidVenuesQuery.ERROR_CODE:
            raise InvalidVenuesQuery(cause=error)
        raise UnexpectedError(cause=error)
