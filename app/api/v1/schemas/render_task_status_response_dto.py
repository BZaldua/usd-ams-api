from datetime import datetime

from pydantic import BaseModel, Field


class RenderTaskStatusResponseDTO(BaseModel):
    task_id: int = Field(..., description="Render task ID", examples=["123"])
    priority: str = Field(..., description="Priorization", examples=["HIGH"])
    status: str = Field(..., description="Render status", examples=["RUNNING"])
    author: str = Field(..., description="Author or requester", examples=["John Doe"])
    created_at: datetime = Field(
        ..., description="Task creation datetime", examples=["2026-07-31T15:30:00Z"]
    )
    finished_at: datetime | None = Field(
        default=None,
        description="Render finished time",
        examples=["2026-07-31T17:50:00Z"],
    )
