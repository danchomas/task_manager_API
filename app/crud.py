from sqlalchemy.orm import Session
from .models import Task
from .schemas import TaskCreate, TaskUpdate
from uuid import UUID


class TaskManager:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: TaskCreate) -> Task:
        db_task = Task(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_task(self, task_id: UUID) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        return self.db.query(Task).offset(skip).limit(limit).all()

    def update_task(self, task_id: UUID, task: TaskUpdate) -> Task | None:
        db_task = self.get_task(task_id)
        if db_task:
            update_data = task.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: UUID) -> Task | None:
        db_task = self.get_task(task_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
        return db_task
