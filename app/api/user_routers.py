from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from schemas.user_schemas import UserCreateSchema, UserLoginSchema, UserSchema, UserLoginResponseSchema
from services.user_services import UserCreateManager, UserLoginManager, UserGetManager
from core.database import get_db
from core.security import auth

router = APIRouter()

@router.get("/all_users")
async def get_users(
    db: Session = Depends(get_db)
) -> List[UserSchema]:
    users = UserGetManager(db).get_all_users()
    return users

@router.get("/{user_id}")
async def get_user_by_id(
    db: Session = Depends(get_db)
    , user_id: UUID = Path(...)
) -> UserSchema:
    user = UserGetManager(db).get_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail="invalid user id")

@router.post("/create_user", response_model=UserSchema)
async def create_user(
    db: Session = Depends(get_db),
    new_user: UserCreateSchema = Depends(UserCreateSchema)
) -> UserSchema:
    user = UserCreateManager(db).create_user(new_user)
    return user

@router.post("/login")
async def login(db: Session = Depends(get_db), user: UserLoginSchema = Depends(UserLoginSchema)):
    result = UserLoginManager(db).login_user(user.username, user.password)
    return {"access": 200}
