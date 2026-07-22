from app.domain import Publish
from app.infrastructure.database import PublishModel
from app.infrastructure.repositories import PublishRepository

from .asset_service import AssetService
from .task_service import TaskService


class PublishService:
    def __init__(
        self,
        publish_repo: PublishRepository,
        asset_service: AssetService,
        task_service: TaskService,
    ):
        self.repository = publish_repo
        self.asset_service = asset_service
        self.task_service = task_service

    async def create(self, publish: Publish) -> Publish:
        task = await self.task_service.get_by_id(publish.task.id)
        asset = await self.asset_service.get_by_id(publish.asset.id)

        latest_version = await self.repository.get_latest_version(asset.id, task.id)

        publish = PublishModel(
            asset_id=asset.id,
            task_id=task.id,
            version=latest_version + 1,
            author=publish.author,
            fs_path="PATH",  # TODO: set a valid path
        )

        published_model: PublishModel = await self.repository.add(publish)

        return Publish(
            task=task,
            asset=asset,
            version=latest_version + 1,
            file_path=published_model.fs_path,
        )
