from app.infrastructure.database import Publish
from app.infrastructure.repositories import PublishRepository
from app.schemas import AssetPublishDTO, AssetPublishResponseDTO
from app.services import AssetService, TaskService


class PublishService:
    def __init__(
        self,
        publish_repo: PublishRepository,
        asset_service: AssetService,
        task_service: TaskService,
    ):
        self.repository = publish_repo

    async def create(self, asset_dto: AssetPublishDTO) -> AssetPublishResponseDTO:
        return AssetPublishResponseDTO(
            name="AA", task="BB", version=1, is_variant=False, filepath="CC"
        )
