# app/schemas.py
from pydantic import BaseModel, UUID4
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    id: UUID4

    class Config:
        from_attributes = True  # For ORM mode
