from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .asset import Asset
from .file_input import FileInput
from .task import Task
from .variant import Variant


@dataclass(frozen=True)
class Publish:
    task: Task
    asset: Asset
    version: int
    file: FileInput
    author: str
    created_at: datetime
    name: str
    type: str
    variants: list[Variant]
    id: Optional[int] = None
