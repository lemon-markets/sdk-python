from lemon.base import Client
from lemon.streaming.model import Token


class StreamingAPI(Client):
    def __init__(
        self,
        api_token: str,
        streaming_api_url: str,
        timeout: float,
        retry_count: int,
        retry_backoff_factor: float,
    ):
        super().__init__(
            base_url=streaming_api_url,
            api_token=api_token,
            timeout=timeout,
            retry_count=retry_count,
            retry_backoff_factor=retry_backoff_factor,
        )

    def authenticate(self) -> Token:
        resp = self.post("auth", json={})
        return Token._from_data(data=resp.json())
