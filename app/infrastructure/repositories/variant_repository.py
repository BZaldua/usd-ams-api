from typing import List

from sqlalchemy.future import select

from app.infrastructure.database import VariantModel
from app.infrastructure.repositories.base import BaseRepository


class VariantRepository(BaseRepository):
    async def get_by_publish_id(self, publish_id: int) -> List[VariantModel]:
        query = select(VariantModel).where(VariantModel.publish_id == publish_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
