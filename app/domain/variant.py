from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    id: int
    name: str
    set: str
