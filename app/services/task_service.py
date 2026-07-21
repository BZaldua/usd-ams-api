from app.exceptions import TaskNotFoundException
from app.infrastructure.database import Task
from app.infrastructure.repositories import TaskRepository
from app.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.repository = task_repo

    async def get_types(self) -> TaskTypesResponseDTO:
        task_lst: list[Task] = await self.repository.get_all()
        types = [TaskTypeResponseDTO(id=task.id, name=task.name) for task in task_lst]
        return TaskTypesResponseDTO(types=types)

    async def get_by_id(self, id: int) -> TaskTypeResponseDTO:
        task: Task = await self.repository.get_by_id(id)
        if not task:
            raise TaskNotFoundException(id)
        return TaskTypeResponseDTO(id=task.id, name=task.name)
