from enum import Enum

from fastapi import Form
from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    asset_name: str = Field(
        ..., min_length=1, max_length=100, description="Asset name", examples=["Hero"]
    )


class AssetCreateDTO(AssetBase):
    pass


class DepartmentType(str, Enum):
    MODEL = "modeling"
    RIG = "rigging"
    ANIMATION = "animation"


class AssetPublishDTO(BaseModel):
    department: DepartmentType = Field(
        ..., description="Department where asset was created", examples=["Modeling"]
    )
    is_variant: bool = Field(default=False)

    @classmethod
    def as_form(
        cls, department: DepartmentType = Form(...), is_variant: bool = Form(...)
    ) -> AssetPublishDTO:
        return cls(department, is_variant)


class AssetPublishResponseDTO(AssetBase):
    department: DepartmentType = Field(
        ..., description="Department where asset was created"
    )
    version: str = Field(description="Version value", default="latest")
    is_variant: bool = Field(default=False)
    filepath: str = Field(..., description="FS path")


class ResolveFilterDTO(AssetBase):
    department: DepartmentType = Field(
        ..., description="Department where asset was created", examples=["Animation"]
    )
    version: str = Field(default="latest", examples=["1.2.1"])
    is_variant: bool = Field(default=False)


class ResolveFilterResponseDTO(BaseModel):
    filepath: str = Field(..., description="FS path")
    signed: bool = Field(default=False)
