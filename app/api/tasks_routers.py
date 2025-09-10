from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from schemas.tasks_schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from schemas.user_schemas import UserSchema, UserBase
from services.tasks_services import TaskCreateManager, TaskGetManager, TaskUpdateManager, TaskDeleteManager
from core.database import get_db
from core.security import auth
from models.user_models import User

router = APIRouter()
'''
@router.post("/my_tasks", response_model=List[TaskSchema], status_code=status.HTTP_200_OK, dependencies=[Depends(security.access_token_required)])
def get_current_user_tasks_endpoint(user: UserBase, db: Session = Depends(get_db)):
    task_manager = TaskGetManager(db)
    return task_manager.get_tasks_user_id(user.id)


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task: TaskCreateSchema, db: Session = Depends(get_db)):
    task_manager = TaskCreateManager(db)
    return task_manager.create_task(task)

@router.get("/{task_id}", response_model=TaskSchema)
def get_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    task_manager = TaskGetManager(db)
    db_task = task_manager.get_task(task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get("/", response_model=List[TaskSchema])
def get_tasks_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    task_manager = TaskGetManager(db)
    return task_manager.get_tasks(skip, limit)


@router.put("/{task_id}", response_model=TaskSchema)
def update_task_endpoint(task_id: UUID, task: TaskUpdateSchema, db: Session = Depends(get_db)):
    task_manager = TaskUpdateManager(db)
    db_task = task_manager.update_task(task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=TaskSchema)
def delete_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    task_manager = TaskDeleteManager(db)
    db_task = task_manager.delete_task(task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
'''
