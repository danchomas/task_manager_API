from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.tasks_models import Task
from schemas.tasks_schemas import TaskCreateSchema, TaskUpdateSchema
from uuid import UUID


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: UUID, user_id: int) -> Task | None:
        return self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

class TaskCreateManager(TaskRepository):
    def create_task(self, task: TaskCreateSchema, user_id: int) -> Task:
        task_data = task.model_dump()
        task_data['user_id'] = user_id
        db_task = Task(**task_data)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

class TaskGetManager(TaskRepository):
    def get_tasks_user_id(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(
            Task.user_id == user_id
        ).all()

class TaskUpdateManager(TaskRepository):
    def update_task(self, task: TaskUpdateSchema, user_id: int, task_id: UUID) -> Task | None:

        db_task = self.get_task(task_id, user_id)

        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh
        return db_task

class TaskDeleteManager(TaskRepository):
    def delete_task(self, task_id: UUID) -> Task | None:
        db_task = self.get_task(task_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
        return db_task
