from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.v1.mappers import TaskMapper
from app.api.v1.schemas import TaskTypesResponseDTO
from app.services import TaskService

router = APIRouter()


@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=TaskTypesResponseDTO,
)
@inject
async def get_types(
    task_service: FromDishka[TaskService], task_mapper: FromDishka[TaskMapper]
):
    tasks = await task_service.get_types()
    result: TaskTypesResponseDTO = task_mapper.to_task_types_response_dto(tasks)
    return result
