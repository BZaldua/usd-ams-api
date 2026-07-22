from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.v1.schemas import AssetPublishDTO, AssetPublishResponseDTO
from app.infrastructure.database import PublishModel
from app.services.publish_service import PublishService


@pytest.fixture
def mock_publish_repo():
    repo = MagicMock()
    repo.get_latest_version = AsyncMock()
    repo.add = AsyncMock()
    return repo


@pytest.fixture
def mock_asset_service():
    service = MagicMock()
    service.get_by_id = AsyncMock()
    return service


@pytest.fixture
def mock_task_service():
    service = MagicMock()
    service.get_by_id = AsyncMock()
    return service


@pytest.fixture
def publish_service(mock_publish_repo, mock_asset_service, mock_task_service):
    return PublishService(
        publish_repo=mock_publish_repo,
        asset_service=mock_asset_service,
        task_service=mock_task_service,
    )


@pytest.mark.asyncio
async def test_create_publish_success(
    publish_service, mock_publish_repo, mock_asset_service, mock_task_service
):
    # Arrange
    publish_dto = AssetPublishDTO(asset_id=1, task_id=10, author="John Doe")

    mock_task = MagicMock()
    mock_task.name = "Modeling"
    mock_task_service.get_by_id.return_value = mock_task

    mock_asset = MagicMock()
    mock_asset.name = "Character_Hero"
    mock_asset_service.get_by_id.return_value = mock_asset

    mock_publish_repo.get_latest_version.return_value = 2

    expected_publish_model = PublishModel(
        asset_id=1, task_id=10, version=3, author="John Doe", fs_path="PATH"
    )
    mock_publish_repo.add.return_value = expected_publish_model

    # Act
    result = await publish_service.create(publish_dto)

    # Assert
    mock_task_service.get_by_id.assert_called_once_with(10)
    mock_asset_service.get_by_id.assert_called_once_with(1)
    mock_publish_repo.get_latest_version.assert_called_once_with(1, 10)

    mock_publish_repo.add.assert_called_once()
    saved_publish = mock_publish_repo.add.call_args[0][0]
    assert saved_publish.asset_id == 1
    assert saved_publish.task_id == 10
    assert saved_publish.version == 3
    assert saved_publish.author == "John Doe"
    assert saved_publish.fs_path == "PATH"

    # 3. Verificar la respuesta DTO devuelta
    assert isinstance(result, AssetPublishResponseDTO)
    assert result.name == "Character_Hero"
    assert result.task == "Modeling"
    assert result.version == 3
    assert result.is_variant is False
    assert result.filepath == "PATH"


@pytest.mark.asyncio
async def test_create_publish_first_version(
    publish_service, mock_publish_repo, mock_asset_service, mock_task_service
):
    # Arrange
    publish_dto = AssetPublishDTO(asset_id=1, task_id=10, author="John Doe")

    mock_task = MagicMock()
    mock_task.name = "Rigging"
    mock_task_service.get_by_id.return_value = mock_task

    mock_asset = MagicMock()
    mock_asset.name = "Sword"
    mock_asset_service.get_by_id.return_value = mock_asset

    mock_publish_repo.get_latest_version.return_value = 0

    expected_publish_model = PublishModel(
        asset_id=1, task_id=10, version=1, author="John Doe", fs_path="PATH"
    )
    mock_publish_repo.add.return_value = expected_publish_model

    # Act
    result = await publish_service.create(publish_dto)

    # Assert
    assert result.version == 1
    saved_publish = mock_publish_repo.add.call_args[0][0]
    assert saved_publish.version == 1
