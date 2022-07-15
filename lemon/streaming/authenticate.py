from datetime import datetime
from typing import List, Optional

from lemon.base import Client
from lemon.streaming.model import Token
from lemon.types import Sorting


class LiveStreaming:
    def __init__(self, client: Client):
        self._client = client

    def get_token(self) -> Token:
        resp = self._client.post("auth", json={})
        return Token._from_data(data=resp.json())
