from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Asset name", examples=["Hero"]
    )
