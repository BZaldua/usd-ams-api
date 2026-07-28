from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: int
    name: str | None = None
