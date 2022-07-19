from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict

from lemon.types import BaseModel


@dataclass
class Token(BaseModel):
    token: str
    user_id: str
    expires_at: datetime
