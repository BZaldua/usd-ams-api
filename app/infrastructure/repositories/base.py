from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, model: Any) -> Any:
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model) 
        return model