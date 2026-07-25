from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.v1.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO
from app.services import TaskService

router = APIRouter()


@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=TaskTypesResponseDTO,
)
@inject
async def get_types(task_service: FromDishka[TaskService]):
    tasks = await task_service.get_types()
    result = [TaskTypeResponseDTO(id=t.id, task=t.name) for t in tasks]
    return TaskTypesResponseDTO(tasks=result)
