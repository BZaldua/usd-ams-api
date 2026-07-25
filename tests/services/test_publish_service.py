import io
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain import Asset, FileInput, Publish, Task
from app.exceptions import NoFilteredContentFoundException
from app.infrastructure.database import PublishModel
from app.services.publish_service import PublishService


@pytest.fixture
def mock_publish_repo():
    repo = MagicMock()
    repo.get_latest_version = AsyncMock()
    repo.get_filtered = AsyncMock()
    repo.add = AsyncMock()
    return repo


@pytest.fixture
def mock_minio_repo():
    repo = MagicMock()
    repo.save = MagicMock()
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
def publish_service(
    mock_publish_repo, mock_asset_service, mock_task_service, mock_minio_repo
):
    return PublishService(
        publish_repo=mock_publish_repo,
        asset_service=mock_asset_service,
        task_service=mock_task_service,
        minio_repository=mock_minio_repo,
    )


@pytest.mark.asyncio
async def test_create_publish_success(
    publish_service,
    mock_publish_repo,
    mock_asset_service,
    mock_task_service,
    mock_minio_repo,
):
    # Arrange
    file_content = b"Test file content"
    mock_file = FileInput(
        filename="test_file",
        content=io.BytesIO(file_content),
        size=len(file_content),
        content_type="text/plain",
    )

    request = Publish(
        asset=Asset(id=1), task=Task(id=10), author="John Doe", file_input=mock_file
    )

    mock_task = MagicMock()
    mock_task.id = 10
    mock_task.name = "Modeling"
    mock_task_service.get_by_id.return_value = mock_task

    mock_asset = MagicMock()
    mock_asset.id = 1
    mock_asset.name = "Character_Hero"
    mock_asset_service.get_by_id.return_value = mock_asset

    mock_publish_repo.get_latest_version.return_value = 2

    fs_file_path = f"{mock_asset.name}/{mock_task.name}/v3/{mock_file.filename}"
    mock_minio_repo.save.return_value = fs_file_path

    expected_publish_model = PublishModel(
        asset_id=1, task_id=10, version=3, author="John Doe", fs_path=fs_file_path
    )
    mock_publish_repo.add.return_value = expected_publish_model

    # Act
    result = await publish_service.create(request)

    # Assert
    mock_task_service.get_by_id.assert_called_once_with(10)
    mock_asset_service.get_by_id.assert_called_once_with(1)
    mock_publish_repo.get_latest_version.assert_called_once_with(1, 10)
    mock_minio_repo.save.asset_called_once()
    mock_publish_repo.add.assert_called_once()
    saved_publish = mock_publish_repo.add.call_args[0][0]
    assert saved_publish.asset_id == 1
    assert saved_publish.task_id == 10
    assert saved_publish.version == 3
    assert saved_publish.author == "John Doe"
    assert saved_publish.fs_path == fs_file_path

    assert isinstance(result, Publish)
    assert result.asset.name == "Character_Hero"
    assert result.task.name == "Modeling"
    assert result.version == 3
    assert result.file_path == fs_file_path


@pytest.mark.asyncio
async def test_create_publish_first_version(
    publish_service,
    mock_publish_repo,
    mock_asset_service,
    mock_task_service,
    mock_minio_repo,
):
    # Arrange
    file_content = b"Test file content"
    mock_file = FileInput(
        filename="test_file",
        content=io.BytesIO(file_content),
        size=len(file_content),
        content_type="text/plain",
    )

    request = Publish(
        asset=Asset(id=1), task=Task(id=10), author="John Doe", file_input=mock_file
    )

    mock_task = MagicMock()
    mock_task.id = 10
    mock_task.name = "Rigging"
    mock_task_service.get_by_id.return_value = mock_task

    mock_asset = MagicMock()
    mock_asset.id = 1
    mock_asset.name = "Sword"
    mock_asset_service.get_by_id.return_value = mock_asset

    mock_publish_repo.get_latest_version.return_value = 0

    fs_file_path = f"{mock_asset.name}/{mock_task.name}/v1/{mock_file.filename}"
    mock_minio_repo.save.return_value = fs_file_path

    expected_publish_model = PublishModel(
        asset_id=1, task_id=10, version=1, author="John Doe", fs_path=fs_file_path
    )
    mock_publish_repo.add.return_value = expected_publish_model

    # Act
    result = await publish_service.create(request)

    # Assert
    mock_minio_repo.save.asset_called_once()
    assert result.version == 1
    saved_publish = mock_publish_repo.add.call_args[0][0]
    assert saved_publish.version == 1


@pytest.mark.asyncio
async def test_get_by_task_and_asset_success(
    publish_service,
    mock_publish_repo,
    mock_asset_service,
    mock_task_service,
):
    # Arrange
    task_id = 10
    asset_id = 1

    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task.name = "Modeling"
    mock_task_service.get_by_id.return_value = mock_task

    mock_asset = MagicMock(spec=Asset)
    mock_asset.id = asset_id
    mock_asset.name = "Character_Hero"
    mock_asset_service.get_by_id.return_value = mock_asset

    mock_publish_model = MagicMock(spec=PublishModel)
    mock_publish_model.id = 100
    mock_publish_model.version = 1
    mock_publish_model.author = "John Doe"

    mock_publish_repo.get_filtered.return_value = [mock_publish_model]

    # Act
    result = await publish_service.get_by_task_and_asset(task_id, asset_id)

    # Assert
    mock_task_service.get_by_id.assert_called_once_with(task_id)
    mock_asset_service.get_by_id.assert_called_once_with(asset_id)
    mock_publish_repo.get_filtered.assert_called_once_with(task_id, asset_id)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Publish)
    assert result[0].id == 100
    assert result[0].version == 1
    assert result[0].author == "John Doe"
    assert result[0].task == mock_task
    assert result[0].asset == mock_asset


@pytest.mark.asyncio
async def test_get_by_task_and_asset_not_found_raises_exception(
    publish_service,
    mock_publish_repo,
    mock_asset_service,
    mock_task_service,
):
    # Arrange
    task_id = 10
    asset_id = 1

    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task_service.get_by_id.return_value = mock_task

    mock_asset = MagicMock(spec=Asset)
    mock_asset.id = asset_id
    mock_asset_service.get_by_id.return_value = mock_asset

    mock_publish_repo.get_filtered.return_value = []

    # Act & Assert
    with pytest.raises(NoFilteredContentFoundException):
        await publish_service.get_by_task_and_asset(task_id, asset_id)

    mock_task_service.get_by_id.assert_called_once_with(task_id)
    mock_asset_service.get_by_id.assert_called_once_with(asset_id)
    mock_publish_repo.get_filtered.assert_called_once_with(task_id, asset_id)
