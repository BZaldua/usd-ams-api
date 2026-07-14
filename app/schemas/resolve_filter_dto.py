from pydantic import Field

from .base import AssetBase, TaskType


class ResolveFilterDTO(AssetBase):
    task: TaskType = Field(
        ..., description="Task where asset was created", examples=["Animation"]
    )
    version: str = Field(default="latest", examples=["1.2.1"])
    is_variant: bool = Field(default=False)
