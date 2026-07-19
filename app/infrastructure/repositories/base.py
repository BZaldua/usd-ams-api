from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, model: Any) -> Any:
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return model
