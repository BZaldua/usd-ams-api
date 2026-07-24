from pydantic import BaseModel, Field


class TaskTypeResponseDTO(BaseModel):
    id: int = Field(..., examples=[2])
    task: str = Field(..., examples=["Rigging"])
