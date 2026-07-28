import pytest
from fastapi import status


class MockTask:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


@pytest.mark.asyncio
async def test_get_types_success(client, task_service_mock):
    # Arrange
    task_service_mock.get_types.return_value = [
        MockTask(id=1, name="Task 1"),
        MockTask(id=2, name="Task 2"),
    ]

    # Act
    response = await client.get("/tasks")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) == 2

    assert data["tasks"][0]["id"] == 1
    assert data["tasks"][0]["task"] == "Task 1"

    assert data["tasks"][1]["id"] == 2
    assert data["tasks"][1]["task"] == "Task 2"
