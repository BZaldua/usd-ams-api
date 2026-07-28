from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import TaskModel
from app.infrastructure.repositories.base import BaseRepository


class TaskRepository(BaseRepository[TaskModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, TaskModel)
