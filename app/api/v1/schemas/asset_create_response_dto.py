from pydantic import BaseModel, Field


class AssetCreateResponseDTO(BaseModel):
    id: int = Field(...)
    name: str = Field(..., description="Asset name", examples=["Hero"])
    type: str = Field(..., description="Type of asset", examples=["Prop"])
