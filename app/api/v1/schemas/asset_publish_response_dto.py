from pydantic import Field

from .base import AssetBase


class AssetPublishResponseDTO(AssetBase):
    task: str = Field(..., description="Task where asset was created")
    version: int = Field(description="Version value", default="latest")
    is_variant: bool = Field(default=False)
    filepath: str = Field(..., description="FS path")
