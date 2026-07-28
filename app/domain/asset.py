from dataclasses import dataclass


@dataclass(frozen=True)
class Asset:
    id: int | None = None
    name: str | None = None
    type: str | None = None
