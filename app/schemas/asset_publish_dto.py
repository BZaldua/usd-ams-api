from fastapi import Form
from pydantic import BaseModel, Field

from .base import TaskType


class AssetPublishDTO(BaseModel):
    task: TaskType = Field(
        ..., description="Task where asset was created", examples=["Modeling"]
    )
    is_variant: bool = Field(default=False)

    @classmethod
    def as_form(
        cls, task: TaskType = Form(...), is_variant: bool = Form(...)
    ) -> AssetPublishDTO:
        return cls(task, is_variant)
