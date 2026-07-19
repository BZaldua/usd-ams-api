from typing import List

from sqlalchemy.future import select

from app.infrastructure.database import Variant
from app.infrastructure.repositories.base import BaseRepository


class VariantRepository(BaseRepository):
    async def get_by_publish_id(self, publish_id: int) -> List[Variant]:
        query = select(Variant).where(Variant.publish_id == publish_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
