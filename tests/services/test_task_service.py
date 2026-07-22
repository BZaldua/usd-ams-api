from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.v1.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO
from app.exceptions import TaskNotFoundException
from app.infrastructure.database import Task
from app.services import TaskService


@pytest.mark.asyncio
async def test_get_types_returns_successfully():
    # Arrange
    mock_task_1 = MagicMock(spec=Task)
    mock_task_1.id = 1
    mock_task_1.name = "Rigging"

    mock_task_2 = MagicMock(spec=Task)
    mock_task_2.id = 2
    mock_task_2.name = "Animation"

    fake_tasks = [mock_task_1, mock_task_2]

    mock_repo = MagicMock()
    mock_repo.get_all = AsyncMock(return_value=fake_tasks)

    service = TaskService(task_repo=mock_repo)

    # Act
    result = await service.get_types()

    # Assert
    mock_repo.get_all.assert_called_once()

    assert isinstance(result, TaskTypesResponseDTO)
    assert len(result.types) == 2

    assert result.types[0].id == 1
    assert result.types[0].name == "Rigging"

    assert result.types[1].id == 2
    assert result.types[1].name == "Animation"


@pytest.mark.asyncio
async def test_get_types_empty_list():
    # Arrange
    mock_repo = MagicMock()
    mock_repo.get_all = AsyncMock(return_value=[])

    service = TaskService(task_repo=mock_repo)

    # Act
    result = await service.get_types()

    # Assert
    mock_repo.get_all.assert_called_once()
    assert isinstance(result, TaskTypesResponseDTO)
    assert len(result.types) == 0


@pytest.mark.asyncio
async def test_get_by_id_successfully():
    # Arrange
    mock_task = MagicMock(spec=Task)
    mock_task.id = 4
    mock_task.name = "Lighting"

    mock_repo = MagicMock()
    mock_repo.get_by_id = AsyncMock(return_value=mock_task)

    service = TaskService(mock_repo)

    # Act
    result = await service.get_by_id(4)

    # Assert
    mock_repo.get_by_id.assert_called_once()

    assert isinstance(result, TaskTypeResponseDTO)
    assert result.id == 4
    assert result.name == "Lighting"


@pytest.mark.asyncio
async def test_get_by_id_should_raise_task_not_found_exception_when_task_does_not_exist():
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_by_id = AsyncMock(return_value=None)

    service = TaskService(repository_mock)
    task_id = 99

    # Act + Assert
    with pytest.raises(TaskNotFoundException) as exc_info:
        await service.get_by_id(task_id)

    repository_mock.get_by_id.assert_called_once_with(task_id)

    assert str(task_id) in str(exc_info.value)
