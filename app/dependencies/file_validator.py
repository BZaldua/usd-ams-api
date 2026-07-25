import os
from pathlib import Path

from fastapi import UploadFile

from app.domain.exceptions import UnsupportedFileFormat


class ValidateFileExtension:

    def __init__(self):
        raw_extensions = os.getenv("FILE_EXTENSIONS", "usd,usda,usdc")

        self.supported_extensions = [
            ext.strip().lower() for ext in raw_extensions.split(",") if ext.strip()
        ]

    async def __call__(self, asset_file: UploadFile) -> UploadFile:
        file_path = Path(asset_file.filename or "")
        ext = file_path.suffix.lower()[1:]

        if ext not in self.supported_extensions:
            raise UnsupportedFileFormat(file_extension=ext)

        return asset_file


validate_file_extension = ValidateFileExtension()
