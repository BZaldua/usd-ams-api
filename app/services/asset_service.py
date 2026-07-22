from app.api.v1.schemas import AssetCreateDTO
from app.exceptions import AssetNotFoundException
from app.infrastructure.database import AssetModel
from app.infrastructure.repositories import AssetRepository


class AssetService:
    def __init__(self, asset_repo: AssetRepository):
        self.repository = asset_repo

    async def create(self, asset_dto: AssetCreateDTO) -> AssetCreateDTO:
        asset_model = AssetModel(name=asset_dto.name, type=asset_dto.type)
        _ = await self.repository.add(asset_model)
        return asset_dto

    async def get_by_id(self, id: int) -> AssetCreateDTO:
        asset_model: AssetModel = await self.repository.get_by_id(id)
        if not asset_model:
            raise AssetNotFoundException(id)
        return AssetCreateDTO(name=asset_model.name, type=asset_model.type)
