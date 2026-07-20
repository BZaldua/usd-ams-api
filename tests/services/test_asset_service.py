from unittest.mock import AsyncMock, MagicMock

import pytest

from app.infrastructure.database import Asset
from app.schemas import AssetCreateDTO
from app.services import AssetService


@pytest.mark.asyncio
async def test_create_returns_successfully():
    # Arrange
    request: AssetCreateDTO = AssetCreateDTO(asset_name="Hero", type="Character")

    mock_model = MagicMock(spec=Asset)
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

    assert isinstance(result, AssetCreateDTO)
    assert result.asset_name == "Hero"
    assert result.type == "Character"


@pytest.mark.asyncio
async def test_get_by_name_successfully():
    # Arrange
    mock_model = MagicMock(spec=Asset)
    mock_model.id = 2
    mock_model.name = "Box"
    mock_model.type = "Prop"

    mock_repo = MagicMock()
    mock_repo.get_by_name = AsyncMock(return_value=mock_model)

    service = AssetService(mock_repo)

    # Act
    result = await service.get_by_name("Box")

    # Assert
    mock_repo.get_by_name.assert_called_once()

    assert isinstance(result, AssetCreateDTO)
    assert result.asset_name == "Box"
    assert result.type == "Prop"
