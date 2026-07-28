import os
from pathlib import Path

from urllib3.response import HTTPResponse

from app.domain import Publish
from app.domain.exceptions import NoFilteredContentFoundException
from app.infrastructure.database import PublishModel
from app.infrastructure.repositories import MinioRepository, PublishRepository

from .asset_service import AssetService
from .task_service import TaskService

_API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
_USDA_TEMPLATE = """#usda 1.0
(
    doc = "Master dynamically by AMS"
    subLayers = [
{sublayers}
    ]
)
"""


class PublishService:
    def __init__(
        self,
        publish_repo: PublishRepository,
        asset_service: AssetService,
        task_service: TaskService,
        minio_repository: MinioRepository,
    ):
        self.repository = publish_repo
        self.asset_service = asset_service
        self.task_service = task_service
        self.minio_repository = minio_repository

    async def create(self, publish: Publish) -> Publish:
        task = await self.task_service.get_by_id(publish.task.id)
        asset = await self.asset_service.get_by_id(publish.asset.id)

        latest_version = await self.repository.get_latest_version(asset.id, task.id)
        new_version = latest_version + 1

        sanitized_filename = publish.file_input.filename.replace(" ", "_").lower()
        object_name = f"{asset.name}/{task.name}/v{new_version}/{sanitized_filename}"

        _ = self.minio_repository.save(
            object_name=object_name,
            content_type=publish.file_input.content_type,
            length=publish.file_input.size,
            data=publish.file_input.content,
        )

        publish = PublishModel(
            asset_id=asset.id,
            task_id=task.id,
            version=new_version,
            author=publish.author,
            fs_path=object_name,
        )

        published_model: PublishModel = await self.repository.add(publish)

        return Publish(
            task=task,
            asset=asset,
            version=latest_version + 1,
            file_path=published_model.fs_path,
            author=published_model.author,
        )

    async def get_by_task_and_asset(self, task_id: int, asset_id: int) -> list[Publish]:
        task = await self.task_service.get_by_id(task_id)
        asset = await self.asset_service.get_by_id(asset_id)

        published_models: list[PublishModel] = await self.repository.get_filtered(
            task.id, asset.id
        )
        if not published_models:
            raise NoFilteredContentFoundException()

        published_result = [
            Publish(task=task, asset=asset, id=p.id, version=p.version, author=p.author)
            for p in published_models
        ]
        return published_result

    async def download(
        self, task_id: int, asset_id: int, version: int
    ) -> tuple[str, HTTPResponse]:
        published_models: list[PublishModel] = await self.repository.get_filtered(
            task_id, asset_id, version
        )
        if not published_models:
            raise NoFilteredContentFoundException()

        object_fs_path = published_models[0].fs_path
        filename: str = Path(object_fs_path).name

        file_content = self.minio_repository.get(object_fs_path)

        return filename, file_content

    async def compose(
        self,
        asset_id: int,
        model_version: int | None = None,
        texture_version: int | None = None,
        rig_version: int | None = None,
        layout_version: int | None = None,
        animation_version: int | None = None,
        vfx_version: int | None = None,
        light_version: int | None = None,
    ) -> tuple[str, str]:
        composition_order = [
            (7, light_version),
            (6, vfx_version),
            (5, animation_version),
            (4, layout_version),
            (3, rig_version),
            (2, texture_version),
            (1, model_version),
        ]

        sublayers = []
        for task in composition_order:
            version = task[1]
            if not version:
                version = await self.repository.get_latest_version(asset_id, task[0])

            if version == 0:
                continue

            asset_download_url: str = (
                f"{_API_BASE_URL}/assets/{asset_id}/{task[0]}/versions/{version}/download"
            )
            sublayers.append(f"\t\t\t@{asset_download_url}@,")

        asset = await self.asset_service.get_by_id(asset_id)
        composed_usda = _USDA_TEMPLATE.format(sublayers="\n".join(sublayers))

        return asset.name, composed_usda
