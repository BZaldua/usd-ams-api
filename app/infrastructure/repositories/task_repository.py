from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import Task
from app.infrastructure.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    async def get_all(self) -> list[Task]:
        query = select(Task)
        result = await self.db.execute(query)
        tasks: list[Task] = list(result.scalars().all())
        return tasks

    async def get_by_name(self, name: str) -> Optional[Task]:
        query = select(Task).where(Task.name == name)
        result = await self.db.execute(query)
        return result.scalars().first()
