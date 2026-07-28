import pytest
from fastapi import status


class MockAsset:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type


class MockTask:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MockPublish:
    def __init__(self, asset, task, version, author):
        self.asset = asset
        self.task = task
        self.version = version
        self.author = author


@pytest.mark.asyncio
async def test_add_asset_success(client, asset_service_mock):
    # Arrange
    asset_service_mock.create.return_value = MockAsset(
        id=1, name="Grass", type="Texture"
    )
    payload = {"name": "Grass", "type": "Texture"}

    # Act
    response = await client.post("/assets", json=payload)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Grass"
    assert data["type"] == "Texture"


@pytest.mark.asyncio
async def test_get_all_assets_success(client, asset_service_mock):
    # Arrange
    asset_service_mock.get_all.return_value = [
        MockAsset(id=1, name="Asset A", type="Character"),
        MockAsset(id=2, name="Asset B", type="Prop"),
    ]

    # Act
    response = await client.get("/assets")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "assets" in data
    assert len(data["assets"]) == 2
    assert data["assets"][0]["name"] == "Asset A"


@pytest.mark.asyncio
async def test_publish_asset_success(client, publish_service_mock):
    # Arrange
    mock_publish = MockPublish(
        asset=MockAsset(id=10, name="Hero", type="Mesh"),
        task=MockTask(id=5, name="Modeling"),
        version=1,
        author="John Doe",
    )
    publish_service_mock.create.return_value = mock_publish

    form_data = {"author": "John Doe"}
    files = {
        "asset_file": (
            "model.usd",
            b"fictional usd content",
            "application/octet-stream",
        )
    }

    # Act
    response = await client.post("/assets/10/5", data=form_data, files=files)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["version"] == 1
    assert data["author"] == "John Doe"
    assert data["asset"]["id"] == 10
    assert data["task"]["id"] == 5


@pytest.mark.asyncio
async def test_get_published_asset_versions_success(client, publish_service_mock):
    # Arrange
    asset_obj = MockAsset(id=20, name="Hero", type="Character")
    task_obj = MockTask(id=7, name="Animation")

    publish_service_mock.get_by_task_and_asset.return_value = [
        MockPublish(asset=asset_obj, task=task_obj, version=1, author="User A"),
        MockPublish(asset=asset_obj, task=task_obj, version=2, author="User B"),
    ]

    # Act
    response = await client.get("/assets/20/7/versions")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["asset"]["id"] == 20
    assert data["task"]["id"] == 7
    assert len(data["versions"]) == 2
    assert data["versions"][0]["version"] == 1
    assert data["versions"][1]["author"] == "User B"


@pytest.mark.asyncio
async def test_download_asset_endpoint_success(client, publish_service_mock):
    # Arrange
    asset_id = 10
    task_id = 5
    version = 1
    expected_filename = "model.usd"
    fake_content = b"fictional usd content"

    publish_service_mock.download.return_value = (expected_filename, [fake_content])

    # Act
    response = await client.get(
        f"/assets/{asset_id}/{task_id}/versions/{version}/download"
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.content == fake_content
    assert response.headers["content-type"] == "application/octet-stream"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{expected_filename}"'
    )

    publish_service_mock.download.assert_called_once_with(asset_id, task_id, version)


@pytest.mark.asyncio
async def test_compose_asset_endpoint_success_with_defaults(
    client, publish_service_mock
):
    # Arrange
    asset_id = 42
    expected_asset_name = "Robot_Hero"
    fake_usda_content = "#usda 1.0\n(\n\tsubLayers = []\n)"

    publish_service_mock.compose.return_value = (
        expected_asset_name,
        [fake_usda_content],
    )

    # Act
    response = await client.get(f"/assets/{asset_id}/compose")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.text == fake_usda_content
    assert response.headers["content-type"] == "application/octet-stream"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{expected_asset_name}_composed.usda"'
    )

    publish_service_mock.compose.assert_called_once_with(
        asset_id, None, None, None, None, None, None, None
    )


@pytest.mark.asyncio
async def test_compose_asset_endpoint_success_with_query_params(
    client, publish_service_mock
):
    # Arrange
    asset_id = 7
    expected_asset_name = "Environment_Forest"
    fake_usda_content = (
        "#usda 1.0\n(\n\tsubLayers = [\n\t\t@/assets/7/1/versions/3/download@\n\t]\n)"
    )

    publish_service_mock.compose.return_value = (
        expected_asset_name,
        [fake_usda_content],
    )

    query_params = {
        "model_version": 3,
        "texture_version": 1,
        "rig_version": 0,
        "layout_version": 2,
        "animation_version": 5,
        "vfx_version": 4,
        "light_version": 1,
    }

    # Act
    response = await client.get(f"/assets/{asset_id}/compose", params=query_params)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.text == fake_usda_content
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{expected_asset_name}_composed.usda"'
    )

    publish_service_mock.compose.assert_called_once_with(asset_id, 3, 1, 0, 2, 5, 4, 1)
