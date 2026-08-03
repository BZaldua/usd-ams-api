from fastapi import UploadFile

from app.api.v1.schemas import (
    AssetCreateDTO,
    AssetCreateResponseDTO,
    AssetListResponseDTO,
    AssetPublishDTO,
    AssetPublishResponseDTO,
    AssetVersionDTO,
    AssetVersionsResponseDTO,
)
from app.domain import Asset, FileInput, Publish, Task

from .task_mapper import TaskMapper


class AssetMapper:

    def __init__(self, task_mapper: TaskMapper):
        self.task_mapper = task_mapper

    def to_asset(self, dto: AssetCreateDTO) -> Asset:
        return Asset(name=dto.name, type=dto.type)

    def to_asset_create_response_dto(self, domain: Asset) -> AssetCreateResponseDTO:
        return AssetCreateResponseDTO(id=domain.id, name=domain.name, type=domain.type)

    def to_asset_list_response_dto(
        self, asset_lst: list[Asset]
    ) -> AssetListResponseDTO:
        asset_create_items = [
            AssetCreateResponseDTO(id=a.id, name=a.name, type=a.type) for a in asset_lst
        ]
        return AssetListResponseDTO(assets=asset_create_items)

    def to_file_input(self, file: UploadFile) -> FileInput:
        return FileInput(
            filename=file.filename,
            content=file.file,
            size=file.size,
            content_type=file.content_type,
        )

    def to_publish(
        self,
        asset_id: int,
        task_id: int,
        file: UploadFile,
        asset_content: AssetPublishDTO,
    ) -> Publish:
        file = self.to_file_input(file)
        asset = Asset(id=asset_id)
        task = Task(id=task_id)
        return Publish(
            asset=asset, task=task, file_input=file, author=asset_content.author
        )

    def to_asset_publish_response_dto(self, domain: Publish) -> AssetPublishResponseDTO:
        asset = self.to_asset_create_response_dto(domain.asset)
        task = self.task_mapper.to_task_types_response_dto(domain.task)
        return AssetPublishResponseDTO(
            asset=asset, task=task, version=domain.version, author=domain.author
        )

    def to_asset_version_dto(self, domain: Publish) -> AssetVersionDTO:
        return AssetVersionDTO(version=domain.version, author=domain.author)

    def to_asset_versions_response_dto(
        self,
        publish_lst: list[Publish],
    ) -> AssetVersionsResponseDTO:
        versions = [self.to_asset_version_dto(p) for p in publish_lst]

        publish = publish_lst[0]
        asset = self.to_asset_create_response_dto(domain=publish.asset)
        task = self.task_mapper.to_task_type_response_dto(domain=publish.task)

        return AssetVersionsResponseDTO(asset=asset, task=task, versions=versions)
