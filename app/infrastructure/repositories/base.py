from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model_class: Type[T]):
        self.db = db
        self.model_class = model_class

    async def add(self, model: T) -> T:
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return model

    async def get_all(self) -> list[T]:
        query = select(self.model_class)
        result = await self.db.execute(query)
        values: list[T] = list(result.scalars().all())
        return values

    async def get_by_id(self, id: int) -> Optional[T]:
        query = select(self.model_class).where(getattr(self.model_class, "id") == id)
        result = await self.db.execute(query)
        return result.scalars().first()
