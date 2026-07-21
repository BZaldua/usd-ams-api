from app.exceptions import AssetNotFoundException
from app.infrastructure.database import Asset
from app.infrastructure.repositories import AssetRepository
from app.schemas import AssetCreateDTO


class AssetService:
    def __init__(self, asset_repo: AssetRepository):
        self.repository = asset_repo

    async def create(self, asset_dto: AssetCreateDTO) -> AssetCreateDTO:
        asset_model = Asset(name=asset_dto.name, type=asset_dto.type)
        _ = await self.repository.add(asset_model)
        return asset_dto

    async def get_by_id(self, id: int) -> AssetCreateDTO:
        asset_model: Asset = await self.repository.get_by_id(id)
        if not asset_model:
            raise AssetNotFoundException(id)
        return AssetCreateDTO(name=asset_model.name, type=asset_model.type)
