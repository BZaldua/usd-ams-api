import os
from dataclasses import dataclass


@dataclass(frozen=True)
class MinioConfig:
    endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("MINIO_ACCESS_KEY")
    secret_key: str = os.getenv("MINIO_SECRET_KEY")
    secure: bool = os.getenv("MINIO_SECURE", "False").lower() in ("true", "1")
    bucket_name: str = os.getenv("MINIO_BUCKET_NAME", "ams")
