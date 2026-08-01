from pydantic import BaseModel, Field


class RenderAssetVersionSelectorDTO(BaseModel):
    model_version: int | None = Field(None, description="Model version", examples=[1])
    texture_version: int | None = Field(None, description="Texture version", examples=[4])
    rig_version: int | None = Field(None, description="Rig version", examples=[2])
    layout_version: int | None = Field(None, description="Layout version", examples=[6])
    animation_version: int | None = Field(
        None, description="Animation version", examples=[4]
    )
    vfx_version: int | None = Field(None, description="VFX version", examples=[1])
    light_version: int | None = Field(None, description="Light version", examples=[1])


class RenderCreateDTO(BaseModel):
    priority: str = Field(..., description="Priorization", examples=["HIGH"])
    author: str = Field(..., description="Author or requester", examples=["John Doe"])
    assets: RenderAssetVersionSelectorDTO = Field(description="Asset versions selector")
