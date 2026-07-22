from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import AssetModel
from app.infrastructure.repositories.base import BaseRepository


class AssetRepository(BaseRepository):
    async def get_by_id(self, id: int) -> Optional[AssetModel]:
        result = await self.db.execute(select(AssetModel).where(AssetModel.id == id))
        return result.scalars().first()
