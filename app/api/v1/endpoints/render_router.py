from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from app.api.v1.schemas import (
    RenderCreateDTO,
    RenderCreateResponseDTO,
    RenderTaskStatusResponseDTO,
    RenderTaskUpdateDTO,
)
from app.services import PublishService

router = APIRouter()


@router.post(
    "/assets/{asset_id}/renders",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=RenderCreateResponseDTO,
)
@inject
async def create_asset_render(
    asset_id: int, payload: RenderCreateDTO, publish_service: FromDishka[PublishService]
):
    return None


@router.get("/assets/{asset_id}/renders/{render_id}", status_code=status.HTTP_200_OK)
@inject
async def get_rendered_asset(
    asset_id: int, render_id: int, publish_service: FromDishka[PublishService]
):
    return None


@router.get(
    "/assets/renders/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=RenderTaskStatusResponseDTO,
)
@inject
async def get_render_status(task_id: int, publish_service: FromDishka[PublishService]):
    return None


@router.put(
    "/assets/renders/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=RenderTaskStatusResponseDTO,
)
@inject
async def update_render_priority(
    task_id: int,
    payload: RenderTaskUpdateDTO,
    publish_service: FromDishka[PublishService],
):
    return None
