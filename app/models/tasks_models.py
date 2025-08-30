import uuid
from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
from enum import Enum


class TaskStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(SQLEnum(TaskStatus, name="taskstatus", values_callable=lambda x: [e.value for e in x]), default=TaskStatus.CREATED)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")
