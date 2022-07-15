from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict

from lemon.types import BaseModel


@dataclass
class Token(BaseModel):
    token: str
    user_id: str
    expires_at: datetime

    @staticmethod
    def _from_data(data: Dict[str, Any]) -> "Token":  # type: ignore # pylint: disable=W0221
        return Token(
            token=data["token"],
            user_id=data["user_id"],
            expires_at=datetime.fromtimestamp(
                data["expires_at"] / 1000, tz=timezone.utc
            ),
        )
