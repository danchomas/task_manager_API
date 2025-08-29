from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user_models import User
from schemas.user_schemas import UserCreateSchema
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

    def login_user(self, email: str, password: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        if user and user.verify_password(password):
            return user
        return None
