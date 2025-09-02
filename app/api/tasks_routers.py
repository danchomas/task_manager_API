from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from schemas.tasks_schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from schemas.user_schemas import UserSchema
from services.tasks_services import TaskCreateManager, TaskGetManager, TaskUpdateManager, TaskDeleteManager
from core.database import get_db
from core.security import security, config
from models.user_models import User

router = APIRouter()

@router.post("/current_user_tasks", response_model=List[TaskSchema], status_code=status.HTTP_200_OK, dependencies=[Depends(security.access_token_required)])
def get_current_user_tasks_endpoint(user: UserSchema, db: Session = Depends(get_db)):
    task_manager = TaskGetManager(db)
    return task_manager.get_tasks_user_id(user.id)
