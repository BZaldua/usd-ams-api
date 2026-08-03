from unittest.mock import MagicMock

import pytest

from app.api.v1.mappers import TaskMapper
from app.api.v1.schemas import TaskTypeResponseDTO, TaskTypesResponseDTO


@pytest.fixture
def mapper():
    return TaskMapper()


@pytest.fixture
def mock_task():
    task = MagicMock()
    task.id = 1
    task.name = "Task"
    return task


@pytest.fixture
def mock_tasks_list():
    tasks = []
    for i in range(1, 3):
        t = MagicMock()
        t.id = i
        t.name = f"Task {i}"
        tasks.append(t)
    return tasks


def test_to_task_type_response_dto_success(mapper, mock_task):
    result = mapper.to_task_type_response_dto(mock_task)

    assert isinstance(result, TaskTypeResponseDTO)
    assert result.id == 1
    assert result.task == "Task"


def test_to_task_types_response_dto_success(mapper, mock_tasks_list):
    result = mapper.to_task_types_response_dto(mock_tasks_list)

    assert isinstance(result, TaskTypesResponseDTO)
    assert len(result.tasks) == 2
    assert all(isinstance(t, TaskTypeResponseDTO) for t in result.tasks)
    assert [t.id for t in result.tasks] == [1, 2]
    assert [t.task for t in result.tasks] == ["Task 1", "Task 2"]


def test_to_task_types_response_dto_empty_list(mapper):
    result = mapper.to_task_types_response_dto([])

    assert isinstance(result, TaskTypesResponseDTO)
    assert len(result.tasks) == 0
