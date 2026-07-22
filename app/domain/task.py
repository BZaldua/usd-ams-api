from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Task:
    id: int
    name: Optional[str] = None
