from dataclasses import dataclass
from datetime import datetime

from .publish import Publish
from .render_priority import RenderPriority
from .render_status import RenderStatus


@dataclass(frozen=True)
class Render:
    assets: list[Publish]
    priority: RenderPriority
    author: str

    id: int | None = None
    status: RenderStatus | None = None
    created_at: datetime | None = None
    finished_at: datetime | None = None
