from pydantic import BaseModel, Field

from .task_type_response_dto import TaskTypeResponseDTO


class TaskTypesResponseDTO(BaseModel):
    types: list[TaskTypeResponseDTO] = Field(...)
