from app.infrastructure.database import Asset
from app.infrastructure.repositories import AssetRepository
from app.schemas import AssetCreateDTO


class AssetService:
    def __init__(self, asset_repo: AssetRepository):
        self.repository = asset_repo

    async def create(self, asset_dto: AssetCreateDTO) -> AssetCreateDTO:
        asset = Asset(name=asset_dto.asset_name, type=asset_dto.type)
        _ = await self.repository.create(asset)
        return asset_dto

    async def get_by_name(self, name: str) -> AssetCreateDTO:
        asset_model: Asset = await self.repository.get_by_name(name)
        return AssetCreateDTO(asset_name=asset_model.name, type=asset_model.type)
