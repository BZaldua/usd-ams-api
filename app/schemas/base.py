from enum import Enum

from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    asset_name: str = Field(
        ..., min_length=1, max_length=100, description="Asset name", examples=["Hero"]
    )


class TaskType(str, Enum):
    MODEL = "modeling"
    RIG = "rigging"
    TEXTURE = "texturing"
    LAYOUT = "layout"
    ANIMATION = "animation"
    VFX = "vfx"
    LIGHT = "lighting"
    RENDER = "rendering"
    COMPOSITE = "compositing"
