from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class FileInput:
    filename: str
    content: BinaryIO
    size: int
    content_type: str
