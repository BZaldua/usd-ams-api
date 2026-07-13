from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import Asset
from app.infrastructure.repositories.base import BaseRepository


class AssetRepository(BaseRepository):
    async def get_by_name(self, name: str) -> Optional[Asset]:
        result = await self.session.execute(select(Asset).where(Asset.name == name))
        return result.scalars().first()

    async def create(self, asset_in: Asset) -> Asset:
        db_asset = Asset(name=asset_in.name, type=asset_in.type.value)
        self.session.add(db_asset)
        await self.session.flush()
        return db_asset
