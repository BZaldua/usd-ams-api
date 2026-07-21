from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import Asset
from app.infrastructure.repositories.base import BaseRepository


class AssetRepository(BaseRepository):
    async def get_by_id(self, id: int) -> Optional[Asset]:
        result = await self.db.execute(select(Asset).where(Asset.id == id))
        return result.scalars().first()
