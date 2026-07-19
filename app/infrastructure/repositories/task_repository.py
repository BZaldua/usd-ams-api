from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import Task
from app.infrastructure.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    async def get_by_name(self, name: str) -> Optional[Task]:
        query = select(Task).where(Task.name == name)
        result = await self.db.execute(query)
        return result.scalars().first()
