from unittest.mock import MagicMock

import pytest
from fastapi import UploadFile

from app.api.v1.mappers.asset_mapper import AssetMapper
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
from app.domain import Asset, FileInput, Publish, Task


@pytest.fixture
def mapper(task_mapper_mock):
    return AssetMapper(task_mapper=task_mapper_mock)


@pytest.fixture
def mock_upload_file():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "geo.usd"
    mock_file.file = "fake_binary_content"
    mock_file.size = 1024
    mock_file.content_type = "application/octet-stream"
    return mock_file


def test_to_asset(mapper):
    dto = AssetCreateDTO(name="Hero", type="character")
    result = mapper.to_asset(dto)

    assert isinstance(result, Asset)
    assert result.name == "Hero"
    assert result.type == "character"


def test_to_asset_create_response_dto(mapper):
    domain = Asset(id=1, name="Chair", type="prop")
    result = mapper.to_asset_create_response_dto(domain)

    assert isinstance(result, AssetCreateResponseDTO)
    assert result.id == 1
    assert result.name == "Chair"
    assert result.type == "prop"


def test_to_asset_list_response_dto(mapper):
    assets = [
        Asset(id=1, name="Tree", type="prop"),
        Asset(id=2, name="Train", type="prop"),
    ]
    result = mapper.to_asset_list_response_dto(assets)

    assert isinstance(result, AssetListResponseDTO)
    assert len(result.assets) == 2
    assert isinstance(result.assets[0], AssetCreateResponseDTO)
    assert [a.id for a in result.assets] == [1, 2]


def test_to_file_input(mapper, mock_upload_file):
    result = mapper.to_file_input(mock_upload_file)

    assert isinstance(result, FileInput)
    assert result.filename == "geo.usd"
    assert result.content == "fake_binary_content"
    assert result.size == 1024
    assert result.content_type == "application/octet-stream"


def test_to_publish(mapper, mock_upload_file):
    dto = AssetPublishDTO(author="John Doe")
    result = mapper.to_publish(
        asset_id=10, task_id=20, file=mock_upload_file, asset_content=dto
    )

    assert isinstance(result, Publish)
    assert result.asset.id == 10
    assert result.task.id == 20
    assert isinstance(result.file_input, FileInput)
    assert result.author == "John Doe"


def test_to_asset_publish_response_dto(mapper, task_mapper_mock):
    domain_asset = Asset(id=1, name="Asset", type="other")
    domain_task = Task(id=2)
    domain_publish = Publish(
        asset=domain_asset,
        task=domain_task,
        file_input=MagicMock(),
        author="Jane Doe",
        version=1,
    )
    mock_task_type_dto = MagicMock(spec=TaskTypeResponseDTO)
    task_mapper_mock.to_task_types_response_dto.return_value = mock_task_type_dto

    result = mapper.to_asset_publish_response_dto(domain_publish)

    assert isinstance(result, AssetPublishResponseDTO)
    assert result.author == "Jane Doe"
    assert result.version == 1
    assert result.task == mock_task_type_dto
    task_mapper_mock.to_task_types_response_dto.assert_called_once_with(domain_task)


def test_to_asset_version_dto(mapper):
    domain_publish = Publish(
        asset=MagicMock(),
        task=MagicMock(),
        file_input=MagicMock(),
        author="Alice",
        version=2,
    )
    result = mapper.to_asset_version_dto(domain_publish)

    assert isinstance(result, AssetVersionDTO)
    assert result.version == 2
    assert result.author == "Alice"


def test_to_asset_versions_response_dto(mapper, task_mapper_mock):
    domain_asset = Asset(id=5, name="Asset", type="type")
    domain_task = Task(id=8, name="task")
    publish_lst = [
        Publish(
            asset=domain_asset,
            task=domain_task,
            file_input=MagicMock(),
            author=f"Author {i}",
            version=i,
        )
        for i in [1, 2]
    ]
    mock_task_dto = MagicMock(spec=TaskTypeResponseDTO)
    task_mapper_mock.to_task_type_response_dto.return_value = mock_task_dto

    result = mapper.to_asset_versions_response_dto(publish_lst)

    assert isinstance(result, AssetVersionsResponseDTO)
    assert len(result.versions) == 2
    assert [v.version for v in result.versions] == [1, 2]
    assert result.task == mock_task_dto
    task_mapper_mock.to_task_type_response_dto.assert_called_once_with(
        domain=domain_task
    )
