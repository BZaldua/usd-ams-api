import logging

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.v1.schemas import TaskTypesResponseDTO
from app.services import TaskService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=TaskTypesResponseDTO,
)
@inject
async def get_types(task_service: FromDishka[TaskService]):
    logger.info("Get task types")
    result = await task_service.get_types()
    logger.debug(f"Task types: {result}")
    return result
