from pydantic import BaseModel, Field

from .asset_create_response_dto import AssetCreateResponseDTO


class AssetListResponseDTO(BaseModel):
    assets: list[AssetCreateResponseDTO] = Field(..., description="Assets list")
