from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.schemas import (
    AssetCreateDTO,
    AssetPublishDTO,
    AssetPublishResponseDTO,
    ResolveFilterDTO,
    ResolveFilterResponseDTO,
)
from app.services import AssetService

router = APIRouter()


@router.post(
    "/assets", status_code=status.HTTP_201_CREATED, response_model=AssetCreateDTO
)
@inject
def add_asset(asset_in: AssetCreateDTO, asset_service: FromDishka[AssetService]):
    return asset_service.create(asset_in)


@router.post(
    "/assets/{asset_name}/publish",
    status_code=status.HTTP_200_OK,
    response_model=AssetPublishResponseDTO,
)
def publish_asset(
    asset_name: str,
    asset_content: AssetPublishDTO = Depends(AssetPublishDTO.as_form),
    asset_file: UploadFile = File(...),
):
    return {"status": "OK", "message": "Asset published"}


@router.get(
    "/assets/resolve",
    status_code=status.HTTP_200_OK,
    response_model=ResolveFilterResponseDTO,
)
def resolve_asset(filters: Annotated[ResolveFilterDTO, Query()]):
    return {"status": "OK", "message": "Asset resolved"}
