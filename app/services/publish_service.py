from app.api.v1.schemas import AssetPublishDTO, AssetPublishResponseDTO
from app.infrastructure.database import Publish
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

    async def create(self, publish_dto: AssetPublishDTO) -> AssetPublishResponseDTO:
        task = await self.task_service.get_by_id(publish_dto.task_id)
        asset = await self.asset_service.get_by_id(publish_dto.asset_id)

        latest_version = await self.repository.get_latest_version(
            publish_dto.asset_id, publish_dto.task_id
        )

        publish = Publish(
            asset_id=publish_dto.asset_id,
            task_id=publish_dto.task_id,
            version=latest_version + 1,
            author=publish_dto.author,
            fs_path="PATH",  # TODO: set a valid path
        )

        published_model: Publish = await self.repository.add(publish)

        return AssetPublishResponseDTO(
            name=asset.name,
            task=task.name,
            version=latest_version + 1,
            is_variant=False,
            filepath=published_model.fs_path,
        )
