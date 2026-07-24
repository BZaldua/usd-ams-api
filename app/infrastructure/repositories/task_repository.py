from app.infrastructure.database import TaskModel
from app.infrastructure.repositories.base import BaseRepository


class TaskRepository(BaseRepository[TaskModel]):
    pass
