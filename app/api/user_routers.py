from fastapi import APIRouter, Depends, HTTPException, status, Path, Security, Body
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserSchema,
    UserUpdateSchema
)
from services.user_services import (
    UserCreateManager,
    UserLoginManager,
    UserGetManager,
    UserUpdateManager
)
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.get("/all_users", dependencies=[Security(auth.verify_token)])
async def get_users(db: Session = Depends(get_db)) -> List[UserSchema]:
    users = UserGetManager(db).get_all_users()
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(
    user_id: UUID = Path(...),
    db: Session = Depends(get_db)
) -> UserSchema:
    user = UserGetManager(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/create_user", response_model=UserSchema)
async def create_user(
    new_user: UserCreateSchema = Body(...),
    db: Session = Depends(get_db)
) -> UserSchema:
    user = UserCreateManager(db).create_user(new_user)
    return user


@router.post("/login")
async def login(
    creds: UserLoginSchema = Body(...),
    db: Session = Depends(get_db)
):
    user = UserLoginManager(db).login_user(creds.username, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_values = {
        "username": user.username,
        "id": user.id
    }
    return {
        "access_token": auth.create_access_token(token_values),
        "token_type": "bearer"
    }


@router.post("/update_user", response_model=UserSchema)
async def update_user(
    creds: UserUpdateSchema = Body(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(auth.verify_token)
):
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    
    updated_user = UserUpdateManager(db).update_user(user_id, creds)
    return updated_user