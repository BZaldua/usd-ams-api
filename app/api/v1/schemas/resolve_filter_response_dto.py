from pydantic import BaseModel, Field


class ResolveFilterResponseDTO(BaseModel):
    filepath: str = Field(..., description="FS path")
    signed: bool = Field(default=False)
