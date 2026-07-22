from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain import Asset
from app.exceptions import AssetNotFoundException
from app.infrastructure.database import AssetModel
from app.services import AssetService


@pytest.mark.asyncio
async def test_create_returns_successfully():
    # Arrange
    request: Asset = Asset(name="Hero", type="Character")

    mock_model = MagicMock(spec=AssetModel)
    mock_model.id = 1
    mock_model.name = "Hero"
    mock_model.type = "Character"

    mock_repo = MagicMock()
    mock_repo.add = AsyncMock(return_value=mock_model)

    service = AssetService(mock_repo)

    # Act
    result = await service.create(request)

    # Assert
    mock_repo.add.assert_called_once()

    assert isinstance(result, Asset)
    assert result.id == 1
    assert result.name == "Hero"
    assert result.type == "Character"


@pytest.mark.asyncio
async def test_get_by_id_successfully():
    # Arrange
    mock_model = MagicMock(spec=AssetModel)
    mock_model.id = 2
    mock_model.name = "Box"
    mock_model.type = "Prop"

    mock_repo = MagicMock()
    mock_repo.get_by_id = AsyncMock(return_value=mock_model)

    service = AssetService(mock_repo)

    # Act
    result = await service.get_by_id(2)

    # Assert
    mock_repo.get_by_id.assert_called_once()

    assert isinstance(result, Asset)
    assert result.id == 2
    assert result.name == "Box"
    assert result.type == "Prop"


@pytest.mark.asyncio
async def test_get_by_id_should_raise_asset_not_found_exception_when_asset_does_not_exist():
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_by_id = AsyncMock(return_value=None)

    service = AssetService(repository_mock)
    asset_id = 99

    # Act + Assert
    with pytest.raises(AssetNotFoundException) as exc_info:
        await service.get_by_id(asset_id)

    repository_mock.get_by_id.assert_called_once_with(asset_id)

    assert str(asset_id) in str(exc_info.value)
