from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from schemas.user_schemas import UserCreateSchema, UserLoginSchema, UserSchema, UserLoginResponseSchema
from services.user_services import UserCreateManager, UserLoginManager, UserGetManager
from core.database import get_db
from core.security import security

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def get_all_users_endpoint(db: Session = Depends(get_db)):
    user_manager = UserGetManager(db)
    return user_manager.get_all_users()

@router.post("/authorization", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_manager = UserCreateManager(db)
    return user_manager.create_user(user)

@router.get("/{user_id}", response_model=UserSchema)
def get_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    user_manager = UserGetManager(db)
    db_user = user_manager.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/login", response_model=UserLoginResponseSchema)
def login_user_endpoint(credentials: UserLoginSchema, db: Session = Depends(get_db)):
    user_manager = UserLoginManager(db)
    db_user = user_manager.login_user(
        credentials.username,
        credentials.password
    )
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = security.create_access_token(uid=str(db_user.id))
    return {"access_token": token}
