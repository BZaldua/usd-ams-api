from app.domain import Task
from app.exceptions import TaskNotFoundException
from app.infrastructure.database import TaskModel
from app.infrastructure.repositories import TaskRepository


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.repository = task_repo

    async def get_types(self) -> list[Task]:
        task_lst: list[TaskModel] = await self.repository.get_all()
        types = [Task(id=t.id, name=t.name) for t in task_lst]
        return types

    async def get_by_id(self, id: int) -> Task:
        task_model: TaskModel = await self.repository.get_by_id(id)
        if not task_model:
            raise TaskNotFoundException(id)
        return Task(id=task_model.id, name=task_model.name)
