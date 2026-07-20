from unittest.mock import AsyncMock, MagicMock

import pytest

from app.infrastructure.database import Task
from app.schemas import TaskTypesResponseDTO
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
