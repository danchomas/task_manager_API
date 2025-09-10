from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from uuid import UUID
from datetime import datetime
import re

class UserBase(BaseModel):
    username: str = Field(
        min_length=4,
        max_length=20
    )
    email: EmailStr

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return value


class UserCreateSchema(UserBase):
    username: str = Field(
        min_length=4,
        max_length=20
    )
    password: str = Field(
        min_length=5
    )

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        pattern = r"^[A-Za-z\d@$!%*?&]{5,}$"
        if not re.match(pattern, value):
            raise ValueError(
                'Password must be at least 5 characters long and contain: '
                'only letters, numbers, and special characters (@$!%*?&)'
            )
        return value


class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserLoginResponseSchema(BaseModel):
    access_token: str

class UserSchema(UserBase):
    id: UUID
    created_at: datetime

class UserSchemaForTasks(BaseModel):
    id: UUID
    username: str

    model_config = ConfigDict(from_attributes=True)
