from app.domain import Asset
from app.domain.exceptions import AssetNotFoundException
from app.infrastructure.database import AssetModel
from app.infrastructure.repositories import AssetRepository


class AssetService:
    def __init__(self, asset_repo: AssetRepository):
        self.repository = asset_repo

    async def get_all(self) -> list[Asset]:
        asset_models: list[AssetModel] = await self.repository.get_all()
        assets = [Asset(id=a.id, name=a.name, type=a.type) for a in asset_models]
        return assets

    async def create(self, asset: Asset) -> Asset:
        new_asset = AssetModel(name=asset.name, type=asset.type)
        saved_asset: AssetModel = await self.repository.add(new_asset)
        return Asset(id=saved_asset.id, name=saved_asset.name, type=saved_asset.type)

    async def get_by_id(self, id: int) -> Asset:
        asset_model: AssetModel = await self.repository.get_by_id(id)
        if not asset_model:
            raise AssetNotFoundException(id)
        return Asset(id=asset_model.id, name=asset_model.name, type=asset_model.type)
