from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Asset:
    name: str
    type: str
    id: Optional[int] = None
