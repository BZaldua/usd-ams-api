from pydantic import BaseModel, Field


class RenderCreateDTO(BaseModel):
    priority: str = Field(..., description="Priorization", examples=["HIGH"])
    author: str = Field(..., description="Author or requester", examples=["John Doe"])
