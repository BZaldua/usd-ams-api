from fastapi import Form
from pydantic import BaseModel, Field


class AssetPublishDTO(BaseModel):
    author: str = Field(description="Author's name")

    @classmethod
    def as_form(
        cls,
        author: str = Form(None, description="Author's name"),
    ) -> "AssetPublishDTO":
        return cls(author=author)
