from pydantic import BaseModel, Field

from .asset_create_response_dto import AssetCreateResponseDTO
from .task_type_response_dto import TaskTypeResponseDTO


class AssetPublishResponseDTO(BaseModel):
    asset: AssetCreateResponseDTO = Field(...)
    task: TaskTypeResponseDTO = Field(...)
    version: int = Field(..., description="Version value")
    author: str = Field(description="Author")
