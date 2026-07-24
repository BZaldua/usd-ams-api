import logging

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, File, UploadFile, status

from app.api.v1.schemas import (
    AssetCreateDTO,
    AssetCreateResponseDTO,
    AssetListResponseDTO,
    AssetPublishDTO,
    AssetPublishResponseDTO,
)
from app.domain import Asset, FileInput, Publish, Task
from app.services import AssetService, PublishService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/assets",
    status_code=status.HTTP_201_CREATED,
    response_model=AssetCreateResponseDTO,
)
@inject
async def add_asset(asset_dto: AssetCreateDTO, asset_service: FromDishka[AssetService]):
    logger.info(f"Creating new asset: {asset_dto}")
    new_asset = Asset(name=asset_dto.name, type=asset_dto.type)
    result = await asset_service.create(new_asset)
    logger.debug(f"Asset creation result: {result}")
    return AssetCreateResponseDTO(id=result.id, name=result.name, type=result.typ)


@router.get(
    "/assets", status_code=status.HTTP_200_OK, response_model=AssetListResponseDTO
)
@inject
async def get_all_assets(asset_service: FromDishka[AssetService]):
    logger.info("Get all assets")
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
    asset_file: UploadFile = File(...),
):
    file = FileInput(
        filename=asset_file.filename,
        content=asset_file.file,
        size=asset_file.size,
        content_type=asset_file.content_type,
    )

    logger.info(
        f"Publish new content={asset_content} for asset={asset_id}, task={task_id}, file={file.filename}"
    )

    publish = Publish(
        asset=Asset(id=asset_id),
        task=Task(id=task_id),
        file_input=file,
        author=asset_content.author,
    )

    result = await publish_service.create(publish)
    logger.debug(f"Publish result: {result}")
    return AssetPublishResponseDTO(
        asset=result.asset,
        task=result.task,
        version=result.version,
        author=result.author,
    )


# @router.get(
#     "/assets/{asset_id}/{task_id}/versions",
#     status_code=status.HTTP_200_OK,
#     response_model=AssetPublishedVersionsResponseDTO,
# )
# @inject
# async def get_published_asset_versions(asset_id: int, task_id: int, asset_service: FromDishka[AssetService]):
#     logger.info(f"Get published task={task_id} asset={asset_id} versions")
#     versions = await asset_service.get_versions(task_id, asset_id)


# @router.get(
#     "/assets/{asset_id}/{task_id}/versions/{version}/download",
#     status_code=status.HTTP_200_OK,
#     response_model=AssetDownloadResponseDTO,
# )
# @inject
# async def download_asset(asset_id: int, task_id: int, version_id: int, asset_service: FromDishka[AssetService]):
#     logger.info(f"Get published task={task_id} asset={asset_id} version={version_id}")
#     versions = await asset_service.download_asset(task_id, asset_id, version_id)


# @router.post(
#     "/assets/{asset_id}/compose",
#     status_code=status.HTTP_200_OK
# )
# @inject
# async def compose_asset(asset_id: int, asset_service: FromDishka[AssetService]):
#     versions = await asset_service.compose_asset(task_id, asset_id)
