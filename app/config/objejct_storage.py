import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectStorageConfig:
    endpoint: str = os.getenv("FS_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("FS_ACCESS_KEY")
    secret_key: str = os.getenv("FS_SECRET_KEY")
    secure: bool = os.getenv("FS_SECURE", "False").lower() in ("true", "1")
    bucket_name: str = os.getenv("FS_BUCKET_NAME", "ams")
