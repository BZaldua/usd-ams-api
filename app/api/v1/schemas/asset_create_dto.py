from pydantic import Field

from .base import AssetBase


class AssetCreateDTO(AssetBase):
    type: str = Field(description="Type of asset", examples=["Prop"])
