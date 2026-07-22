from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import TaskModel
from app.infrastructure.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    async def get_all(self) -> list[TaskModel]:
        query = select(TaskModel)
        result = await self.db.execute(query)
        tasks: list[TaskModel] = list(result.scalars().all())
        return tasks

    async def get_by_id(self, id: int) -> Optional[TaskModel]:
        query = select(TaskModel).where(TaskModel.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()
