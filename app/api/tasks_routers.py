from fastapi import APIRouter, Depends, HTTPException, status, Security, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from schemas.tasks_schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from services.tasks_services import (
    TaskCreateManager,
    TaskGetManager,
    TaskUpdateManager,
    TaskDeleteManager
)
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/my_tasks", response_model=List[TaskSchema])
async def get_current_user_tasks_endpoint(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
) -> List[TaskSchema]:
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    task_manager = TaskGetManager(db)
    return task_manager.get_tasks_user_id(user_id)


@router.post("/create_task", response_model=TaskSchema)
async def create_task(
    task: TaskCreateSchema = Body(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
) -> TaskSchema:
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    task_manager = TaskCreateManager(db)
    return task_manager.create_task(task, user_id)


@router.post("/update_task", response_model=TaskSchema)
async def update_task(
    task: TaskUpdateSchema = Body(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
) -> TaskSchema:
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    task_manager = TaskUpdateManager(db)
    return task_manager.update_task(task, user_id, task.id)


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    task_manager = TaskDeleteManager(db)
    success = task_manager.delete_task(task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return {"detail": "Task deleted successfully"}