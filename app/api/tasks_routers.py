from re import L
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from schemas.tasks_schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from schemas.user_schemas import UserSchema, UserBase
from services.tasks_services import TaskCreateManager, TaskGetManager, TaskUpdateManager, TaskDeleteManager
from core.database import get_db
from core.security import auth
from models.tasks_models import TaskStatus

router = APIRouter()


@router.post("/my_tasks")
async def get_current_user_tasks_endpoint(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
) -> List[TaskSchema]:
    user_id = payload.get('id')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")

    task_manager = TaskGetManager(db)
    return task_manager.get_tasks_user_id(user_id)

@router.post("/create_task")
async def create_task(
    db: Session = Depends(get_db),
    task: TaskCreateSchema = Depends(TaskCreateSchema),
    payload: dict = Depends(auth.verify_token)
) -> TaskSchema:
    user_id = payload.get('id')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user id not found in token")

    task_manager = TaskCreateManager(db)
    return task_manager.create_task(task, user_id)


@router.post("/update_task")
async def update_task(
    task: TaskUpdateSchema,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
) -> TaskSchema:
    user_id = payload.get('id')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


    task_manager = TaskUpdateManager(db)
    return task_manager.update_task(task, user_id, task.id)
