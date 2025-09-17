from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user_models import User
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema
from uuid import UUID
from fastapi import HTTPException, status

class UserCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreateSchema) -> User:
        existing_user = self.db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()

        if existing_user:
            if existing_user.email == user.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        db_user = User(
            email=user.email,
            username=user.username,
            password=user.password
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

class UserGetManager:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: UUID) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

class UserLoginManager:
    def __init__(self, db: Session):
        self.db = db

    def login_user(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if user and user.password == password:
            return user
        return None

class UserUpdateManager:
    def __init__(self, db: Session):
        self.db = db

    def update_user(self, id: str, user: UserUpdateSchema) -> User:
        # Находим пользователя для обновления
        existing_user = self.db.query(User).filter(User.id == id).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Проверяем конфликты email/username у других пользователей
        if user.email:
            # Проверяем email у других пользователей
            email_conflict = self.db.query(User).filter(
                User.email == user.email,
                User.id != id  # исключаем текущего пользователя
            ).first()
            if email_conflict:
                raise HTTPException(status_code=400, detail="Email is already registered")

        if user.username:
            # Проверяем username у других пользователей
            username_conflict = self.db.query(User).filter(
                User.username == user.username,
                User.id != id  # исключаем текущего пользователя
            ).first()
            if username_conflict:
                raise HTTPException(status_code=400, detail="Username is already registered")

        # Обновляем только переданные поля
        update_data = user.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_user, field, value)

        try:
            self.db.commit()
            self.db.refresh(existing_user)
            return existing_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error")
