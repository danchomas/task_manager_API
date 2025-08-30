from pydantic import BaseModel, UUID4, ConfigDict
from enum import Enum
from typing import Optional
from .user_schemas import UserSchema

class TaskStatusSchema(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: TaskStatusSchema = TaskStatusSchema.CREATED

class TaskCreateSchema(TaskBase):
    user_id: UUID4

class TaskUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatusSchema] = None
    user_id: Optional[UUID4] = None

class TaskSchema(TaskBase):
    id: UUID4
    user_id: UUID4
    user: Optional[UserSchema] = None

    model_config = ConfigDict(from_attributes=True)
