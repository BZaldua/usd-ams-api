from fastapi import Form
from pydantic import BaseModel, Field


class AssetPublishDTO(BaseModel):
    asset_id: int = Field(..., description="Asset ID")
    task_id: int = Field(..., description="Task ID")
    author: str = Field(description="Author's name")

    @classmethod
    def as_form(
        cls,
        asset_id: int = Form(..., description="Asset ID"),
        task_id: int = Form(..., description="Task ID"),
        author: str = Form(None, description="Author's name"),
    ) -> "AssetPublishDTO":
        return cls(asset_id=asset_id, task_id=task_id, author=author)
