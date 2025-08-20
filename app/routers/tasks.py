from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..schemas import Task, TaskCreate, TaskUpdate
from ..crud import create_task, get_task, get_tasks, update_task, delete_task
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.get("/{task_id}", response_model=Task)
def get_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get("/", response_model=List[Task])
def get_tasks_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tasks(db, skip, limit)


@router.put("/{task_id}", response_model=Task)
def update_task_endpoint(task_id: UUID, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=Task)
def delete_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    db_task = delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
