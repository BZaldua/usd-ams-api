from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Asset:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
