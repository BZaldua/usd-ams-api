from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .asset import Asset
from .file_input import FileInput
from .task import Task


@dataclass(frozen=True)
class Publish:
    task: Task
    asset: Asset

    id: Optional[int] = None
    version: Optional[int] = None
    author: Optional[str] = None
    file_input: Optional[FileInput] = None
    file_path: Optional[str] = None
    created_at: Optional[datetime] = None
