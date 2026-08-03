from app.api.v1.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO
from app.domain import Task


class TaskMapper:

    def to_task_types_response_dto(self, tasks_lst: list[Task]) -> TaskTypesResponseDTO:
        task_dtos = [self.to_task_type_response_dto(t) for t in tasks_lst]
        return TaskTypesResponseDTO(tasks=task_dtos)

    def to_task_type_response_dto(self, domain: Task) -> TaskTypeResponseDTO:
        return TaskTypeResponseDTO(id=domain.id, task=domain.name)
