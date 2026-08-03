from enum import Enum


class RenderStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3
    CANCELLED = 4
