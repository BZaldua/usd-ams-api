from app.domain import Publish
from app.infrastructure.database import PublishModel
from app.infrastructure.repositories import MinioRepository, PublishRepository

from .asset_service import AssetService
from .task_service import TaskService


class PublishService:
    def __init__(
        self,
        publish_repo: PublishRepository,
        asset_service: AssetService,
        task_service: TaskService,
        minio_repository: MinioRepository,
    ):
        self.repository = publish_repo
        self.asset_service = asset_service
        self.task_service = task_service
        self.minio_repository = minio_repository

    async def create(self, publish: Publish) -> Publish:
        task = await self.task_service.get_by_id(publish.task.id)
        asset = await self.asset_service.get_by_id(publish.asset.id)

        latest_version = await self.repository.get_latest_version(asset.id, task.id)

        sanitized_filename = publish.file_input.filename.replace(" ", "_").lower()
        object_name = f"{asset.name}/{task.name}/{sanitized_filename}_v{latest_version}"

        fs_path = self.minio_repository.save(
            object_name=object_name,
            content_type=publish.file_input.content_type,
            length=publish.file_input.size,
            data=publish.file_input.content,
        )

        publish = PublishModel(
            asset_id=asset.id,
            task_id=task.id,
            version=latest_version + 1,
            author=publish.author,
            fs_path=fs_path,
        )

        published_model: PublishModel = await self.repository.add(publish)

        return Publish(
            task=task,
            asset=asset,
            version=latest_version + 1,
            file_path=published_model.fs_path,
        )
