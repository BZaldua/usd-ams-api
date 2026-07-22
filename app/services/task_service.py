from app.api.v1.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO
from app.exceptions import TaskNotFoundException
from app.infrastructure.database import TaskModel
from app.infrastructure.repositories import TaskRepository


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.repository = task_repo

    async def get_types(self) -> TaskTypesResponseDTO:
        task_lst: list[TaskModel] = await self.repository.get_all()
        types = [TaskTypeResponseDTO(id=task.id, name=task.name) for task in task_lst]
        return TaskTypesResponseDTO(types=types)

    async def get_by_id(self, id: int) -> TaskTypeResponseDTO:
        task: TaskModel = await self.repository.get_by_id(id)
        if not task:
            raise TaskNotFoundException(id)
        return TaskTypeResponseDTO(id=task.id, name=task.name)
