import logging

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.api.v1.schemas import AssetCreateDTO, AssetPublishDTO, AssetPublishResponseDTO
from app.domain import Asset, FileInput, Publish, Task
from app.services import AssetService, PublishService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/assets", status_code=status.HTTP_201_CREATED, response_model=AssetCreateDTO
)
@inject
async def add_asset(asset_dto: AssetCreateDTO, asset_service: FromDishka[AssetService]):
    logger.info(f"Creating new asset: {asset_dto}")
    new_asset = Asset(name=asset_dto.name, type=asset_dto.type)
    result = await asset_service.create(new_asset)
    logger.debug(f"Asset creation result: {result}")
    return AssetCreateDTO(name=result.name, type=result.typ)


@router.post(
    "/assets/{asset_id}/{task_id}",
    status_code=status.HTTP_200_OK,
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
        name=result.asset.name,
        task=result.task.name,
        version=result.version,
    )
