from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Query, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.v1.schemas import (
    AssetCreateDTO,
    AssetCreateResponseDTO,
    AssetListResponseDTO,
    AssetPublishDTO,
    AssetPublishResponseDTO,
    AssetVersionDTO,
    AssetVersionsResponseDTO,
    TaskTypeResponseDTO,
)
from app.dependencies import validate_file_extension
from app.domain import Asset, FileInput, Publish, Task
from app.services import AssetService, PublishService

router = APIRouter()


@router.post(
    "/assets",
    status_code=status.HTTP_201_CREATED,
    response_model=AssetCreateResponseDTO,
)
@inject
async def add_asset(asset_dto: AssetCreateDTO, asset_service: FromDishka[AssetService]):
    new_asset = Asset(name=asset_dto.name, type=asset_dto.type)
    result = await asset_service.create(new_asset)
    return AssetCreateResponseDTO(id=result.id, name=result.name, type=result.type)


@router.get(
    "/assets", status_code=status.HTTP_200_OK, response_model=AssetListResponseDTO
)
@inject
async def get_all_assets(asset_service: FromDishka[AssetService]):
    assets = await asset_service.get_all()
    result = [AssetCreateResponseDTO(id=a.id, name=a.name, type=a.type) for a in assets]
    return AssetListResponseDTO(assets=result)


@router.post(
    "/assets/{asset_id}/{task_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=AssetPublishResponseDTO,
)
@inject
async def publish_asset(
    publish_service: FromDishka[PublishService],
    asset_id: int,
    task_id: int,
    asset_content: AssetPublishDTO = Depends(AssetPublishDTO.as_form),
    asset_file: UploadFile = Depends(validate_file_extension),
):
    file = FileInput(
        filename=asset_file.filename,
        content=asset_file.file,
        size=asset_file.size,
        content_type=asset_file.content_type,
    )

    publish = Publish(
        asset=Asset(id=asset_id),
        task=Task(id=task_id),
        file_input=file,
        author=asset_content.author,
    )

    result = await publish_service.create(publish)
    return AssetPublishResponseDTO(
        asset=AssetCreateResponseDTO(
            id=result.asset.id, name=result.asset.name, type=result.asset.type
        ),
        task=TaskTypeResponseDTO(id=result.task.id, task=result.task.name),
        version=result.version,
        author=result.author,
    )


@router.get(
    "/assets/{asset_id}/{task_id}/versions",
    status_code=status.HTTP_200_OK,
    response_model=AssetVersionsResponseDTO,
)
@inject
async def get_published_asset_versions(
    asset_id: int, task_id: int, publish_service: FromDishka[PublishService]
):
    published_assets = await publish_service.get_by_task_and_asset(task_id, asset_id)
    asset = AssetCreateResponseDTO(
        id=published_assets[0].asset.id,
        name=published_assets[0].asset.name,
        type=published_assets[0].asset.type,
    )
    task = TaskTypeResponseDTO(
        id=published_assets[0].task.id, task=published_assets[0].task.name
    )
    result = AssetVersionsResponseDTO(
        asset=asset,
        task=task,
        versions=[
            AssetVersionDTO(version=pa.version, author=pa.author)
            for pa in published_assets
        ],
    )
    return result


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
