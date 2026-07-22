from typing import BinaryIO

from minio import Minio


class MinioRepository:
    def __init__(self, client: Minio, bucket_name: str):
        self.client = client
        self.bucket = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def save(
        self, object_name: str, data: BinaryIO, length: int, content_type: str
    ) -> str:
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=data,
            length=length,
            content_type=content_type,
        )
        return f"/{self.bucket}/{object_name}"
