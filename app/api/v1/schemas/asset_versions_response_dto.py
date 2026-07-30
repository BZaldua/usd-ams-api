from pydantic import BaseModel, Field

from .asset_create_response_dto import AssetCreateResponseDTO
from .task_type_response_dto import TaskTypeResponseDTO


class AssetVersionDTO(BaseModel):
    version: int = Field(..., description="Version number")
    author: str = Field(description="Version author name")


class AssetVersionsResponseDTO(BaseModel):
    asset: AssetCreateResponseDTO = Field(...)
    task: TaskTypeResponseDTO = Field(...)
    versions: list[AssetVersionDTO] = Field(..., description="Existing versions")
