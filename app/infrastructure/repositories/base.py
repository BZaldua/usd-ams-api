from typing import Generic, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, model: T) -> T:
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return model

    async def get_all(self) -> list[T]:
        query = select(T)
        result = await self.db.execute(query)
        tasks: list[T] = list(result.scalars().all())
        return tasks

    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self.db.execute(select(T).where(T.id == id))
        return result.scalars().first()
