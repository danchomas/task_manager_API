from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserCreateSchema(BaseModel):
    username: str = Field(
        min_length=4,
        max_length=20
    )
    email: EmailStr
    password: str = Field()

    @validator('password')
    def validate_password(cls, value):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]$", value):
            raise ValueError('Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character')
        return value

    @validator('username')
    def validate_username(cls, value):
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return value


class UserLoginSchema(BaseModel):
    username: str
    password: str
