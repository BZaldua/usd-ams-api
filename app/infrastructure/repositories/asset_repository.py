from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import Asset
from app.infrastructure.repositories.base import BaseRepository


class AssetRepository(BaseRepository):
    async def get_by_name(self, name: str) -> Optional[Asset]:
        result = await self.db.execute(select(Asset).where(Asset.name == name))
        return result.scalars().first()

    async def create(self, asset_name: str, asset_type: str) -> Asset:
        db_asset = Asset(name=asset_name, type=asset_type)
        self.db.add(db_asset)
        await self.db.flush()
        return db_asset
