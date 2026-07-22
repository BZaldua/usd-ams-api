from pydantic import BaseModel, Field


class TaskTypeResponseDTO(BaseModel):
    id: int = Field(..., examples=[2])
    name: str = Field(..., examples=["Rigging"])
