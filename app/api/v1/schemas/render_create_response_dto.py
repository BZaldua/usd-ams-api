from pydantic import BaseModel, Field


class RenderCreateResponseDTO(BaseModel):
    task_id: int = Field(..., description="Render task ID", examples=["123"])
