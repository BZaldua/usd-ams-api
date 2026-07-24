from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import AssetModel
from app.infrastructure.repositories.base import BaseRepository


class AssetRepository(BaseRepository[AssetModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, AssetModel)
