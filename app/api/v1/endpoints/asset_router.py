from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Query, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.v1.mappers import AssetMapper
from app.api.v1.schemas import (
    AssetCreateDTO,
    AssetCreateResponseDTO,
    AssetListResponseDTO,
    AssetPublishDTO,
    AssetPublishResponseDTO,
    AssetVersionsResponseDTO,
)
from app.dependencies import validate_file_extension
from app.domain import Asset
from app.services import AssetService, PublishService

router = APIRouter()


@router.post(
    "/assets",
    status_code=status.HTTP_201_CREATED,
    response_model=AssetCreateResponseDTO,
)
@inject
async def add_asset(
    asset_dto: AssetCreateDTO,
    asset_service: FromDishka[AssetService],
    asset_mapper: FromDishka[AssetMapper],
):
    new_asset: Asset = asset_mapper.to_asset(asset_dto)
    result = await asset_service.create(new_asset)
    return asset_mapper.to_asset_create_response_dto(result)


@router.get(
    "/assets", status_code=status.HTTP_200_OK, response_model=AssetListResponseDTO
)
@inject
async def get_all_assets(
    asset_service: FromDishka[AssetService], asset_mapper: FromDishka[AssetMapper]
):
    assets = await asset_service.get_all()
    return asset_mapper.to_asset_list_response_dto(assets)


@router.post(
    "/assets/{asset_id}/{task_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=AssetPublishResponseDTO,
)
@inject
async def publish_asset(
    publish_service: FromDishka[PublishService],
    asset_mapper: FromDishka[AssetMapper],
    asset_id: int,
    task_id: int,
    asset_content: AssetPublishDTO = Depends(AssetPublishDTO.as_form),
    asset_file: UploadFile = Depends(validate_file_extension),
):
    publish = asset_mapper.to_publish(asset_id, task_id, asset_file, asset_content)
    result = await publish_service.create(publish)
    return asset_mapper.to_asset_publish_response_dto(result)


@router.get(
    "/assets/{asset_id}/{task_id}/versions",
    status_code=status.HTTP_200_OK,
    response_model=AssetVersionsResponseDTO,
)
@inject
async def get_published_asset_versions(
    asset_id: int,
    task_id: int,
    publish_service: FromDishka[PublishService],
    asset_mapper: FromDishka[AssetMapper],
):
    published_assets = await publish_service.get_by_task_and_asset(task_id, asset_id)
    return asset_mapper.to_asset_versions_response_dto(published_assets)


@router.get(
    "/assets/{asset_id}/{task_id}/versions/{version}/download",
    status_code=status.HTTP_200_OK,
)
@inject
async def download_asset(
    asset_id: int,
    task_id: int,
    version: int,
    publish_service: FromDishka[PublishService],
):
    filename, file_content = await publish_service.download(asset_id, task_id, version)

    return StreamingResponse(
        content=file_content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/assets/{asset_id}/compose", status_code=status.HTTP_200_OK)
@inject
async def compose_asset(
    asset_id: int,
    publish_service: FromDishka[PublishService],
    model_version: int | None = Query(default=None, description="Model version"),
    texture_version: int | None = Query(default=None, description="Texture version"),
    rig_version: int | None = Query(default=None, description="Rig version"),
    layout_version: int | None = Query(default=None, description="Layout version"),
    animation_version: int | None = Query(
        default=None, description="Animation version"
    ),
    vfx_version: int | None = Query(default=None, description="VFX version"),
    light_version: int | None = Query(default=None, description="Light version"),
):
    asset_name, composed_content = await publish_service.compose(
        asset_id,
        model_version,
        texture_version,
        rig_version,
        layout_version,
        animation_version,
        vfx_version,
        light_version,
    )

    return StreamingResponse(
        content=composed_content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{asset_name}_composed.usda"'
        },
    )
