from pydantic import BaseModel, UUID4, ConfigDict
from enum import Enum
from typing import Optional


class TaskStatusSchema(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: TaskStatusSchema = TaskStatusSchema.CREATED


class TaskCreateSchema(TaskBase):
    pass


class TaskUpdateSchema(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatusSchema] = None


class TaskSchema(TaskBase):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)
