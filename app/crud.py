from sqlalchemy.orm import Session
from .models import Task
from .schemas import TaskCreate, TaskUpdate
from uuid import UUID


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: UUID) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    return db.query(Task).offset(skip).limit(limit).all()


def update_task(db: Session, task_id: UUID, task: TaskUpdate) -> Task | None:
    db_task = get_task(db, task_id)
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: UUID) -> Task | None:
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
