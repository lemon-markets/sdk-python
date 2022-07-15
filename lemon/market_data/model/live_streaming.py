from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Union

from lemon.types import BaseModel

@dataclass
class Token(BaseModel):
    token: str
    user_id: str
    expires_at: datetime

    @staticmethod
    def _from_data(  # type: ignore # pylint: disable=W0221
        data: Dict[str, Any]
    ) -> "Token":
        return Token(
            token=data['token'],
            user_id=data['user_id'],
            expires_at=datetime.fromtimestamp(data['expires_at'] / 1000)
        )
