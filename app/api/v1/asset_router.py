import logging
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

logger = logging.getLogger(__name__)


@router.post(
    "/assets", 
    status_code=status.HTTP_201_CREATED, 
    response_model=AssetCreateDTO
)
@inject
async def add_asset(asset_in: AssetCreateDTO, asset_service: FromDishka[AssetService]):
    logger.info(f"Creating new asset: {asset_in}")
    result = await asset_service.create(asset_in)
    logger.debug(f"Asset creation result: {result}")
    return result


@router.post(
    "/assets/publish",
    status_code=status.HTTP_200_OK,
    response_model=AssetPublishResponseDTO,
)
def publish_asset(
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
