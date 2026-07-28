from pydantic import BaseModel, Field


class AssetCreateDTO(BaseModel):
    name: str = Field(..., description="Asset name", examples=["Hero"])
    type: str = Field(..., description="Type of asset", examples=["Prop"])
