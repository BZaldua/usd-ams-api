import os
from unittest.mock import MagicMock, patch

import pytest

from app.dependencies.file_validator import ValidateFileExtension
from app.domain.exceptions import UnsupportedFileFormat


@pytest.mark.asyncio
async def test_validator_initialization_and_success():
    # Arrange + Act
    with patch.dict(os.environ, {"FILE_EXTENSIONS": "usd,usda,usdc"}):
        validator = ValidateFileExtension()

    # Assert
    assert validator.supported_extensions == ["usd", "usda", "usdc"]

    # Arrange
    mock_file = MagicMock()
    mock_file.filename = "model.USDA"

    # Act
    result = await validator(mock_file)

    # Assert
    assert result == mock_file


@pytest.mark.asyncio
async def test_validator_raises_unsupported_file_format_exception():
    # Arrange
    with patch.dict(os.environ, {"FILE_EXTENSIONS": "usd,usda"}):
        validator = ValidateFileExtension()

    mock_file = MagicMock()
    mock_file.filename = "malicious_payload.exe"

    # Act & Assert
    with pytest.raises(UnsupportedFileFormat) as _:
        await validator(mock_file)


@pytest.mark.asyncio
async def test_validator_handles_pipeline_multidot_filenames():
    # Arrange
    with patch.dict(os.environ, {"FILE_EXTENSIONS": "usd"}):
        validator = ValidateFileExtension()

    mock_file = MagicMock()
    mock_file.filename = "character.shading.v002.usd"

    # Act
    result = await validator(mock_file)

    # Assert
    assert result == mock_file


@pytest.mark.asyncio
async def test_validator_fails_with_no_extension_files():
    # Arrange
    with patch.dict(os.environ, {"FILE_EXTENSIONS": "usdc"}):
        validator = ValidateFileExtension()

    mock_file = MagicMock()
    mock_file.filename = "usd_binary_without_extension"

    # Act & Assert
    with pytest.raises(UnsupportedFileFormat):
        await validator(mock_file)
