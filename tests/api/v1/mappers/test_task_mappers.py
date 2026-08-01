from unittest.mock import MagicMock

import pytest

from app.api.v1.mappers import TaskMapper
from app.api.v1.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO


@pytest.fixture
def mock_task():
    task = MagicMock()
    task.id = 1
    task.name = "Task"
    return task


@pytest.fixture
def mock_tasks_list():
    task1 = MagicMock()
    task1.id = 1
    task1.name = "Task 1"

    task2 = MagicMock()
    task2.id = 2
    task2.name = "Task 2"

    return [task1, task2]


def test_to_task_type_response_dto_success(mock_task):
    # Arrange
    mapper = TaskMapper()

    # Act
    result = mapper.to_task_type_response_dto(mock_task)

    # Assert
    assert isinstance(result, TaskTypeResponseDTO)
    assert result.id == 1
    assert result.task == "Task"


def test_to_task_types_response_dto_success(mock_tasks_list):
    # Arrange
    mapper = TaskMapper()

    # Act
    result = mapper.to_task_types_response_dto(mock_tasks_list)

    # Assert
    assert isinstance(result, TaskTypesResponseDTO)
    assert len(result.tasks) == 2

    assert isinstance(result.tasks[0], TaskTypeResponseDTO)
    assert result.tasks[0].id == 1
    assert result.tasks[0].task == "Task 1"

    assert isinstance(result.tasks[1], TaskTypeResponseDTO)
    assert result.tasks[1].id == 2
    assert result.tasks[1].task == "Task 2"


def test_to_task_types_response_dto_empty_list():
    # Arrange
    mapper = TaskMapper()

    # Act
    result = mapper.to_task_types_response_dto([])

    # Assert
    assert isinstance(result, TaskTypesResponseDTO)
    assert len(result.tasks) == 0
