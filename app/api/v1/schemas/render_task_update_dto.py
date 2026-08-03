from pydantic import BaseModel, Field


class RenderTaskUpdateDTO(BaseModel):
    priority: str = Field(..., description="Priorization", examples=["HIGH"])
