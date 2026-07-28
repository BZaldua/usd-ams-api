from dataclasses import dataclass
from datetime import datetime

from .asset import Asset
from .file_input import FileInput
from .task import Task


@dataclass(frozen=True)
class Publish:
    task: Task
    asset: Asset

    id: int | None = None
    version: int | None = None
    author: str | None = None
    file_input: FileInput | None = None
    file_path: str | None = None
    created_at: datetime | None = None
