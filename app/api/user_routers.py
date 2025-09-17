from fastapi import APIRouter, Depends, HTTPException, status, Path, Security
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional, Dict

from schemas.user_schemas import UserCreateSchema, UserLoginSchema, UserSchema, UserUpdateSchema
from services.user_services import UserCreateManager, UserLoginManager, UserGetManager, UserUpdateManager
from core.database import get_db
from core.security import auth

router = APIRouter()

@router.get("/all_users", dependencies=[Security(auth.verify_token)])
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
async def login(db: Session = Depends(get_db), creds: UserLoginSchema = Depends(UserLoginSchema)):
    user = UserLoginManager(db).login_user(creds.username, creds.password)
    if user:
        token_values = {
            "username": user.username,
            "id": user.id
        }
        return {
            "token": auth.create_access_token(token_values),
            "type": "Bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="invalid credentials")

@router.post("/update_user")
async def update_user(db: Session = Depends(get_db), creds: UserUpdateSchema = Depends(UserUpdateSchema), payload: dict = Depends(auth.verify_token)):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="i cant find this user")
    new_user = UserUpdateManager(db).update_user(user_id, creds)
    return new_user
