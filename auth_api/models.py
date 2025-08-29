from pydantic import BaseModel, EmailStr, Field
import regex

class User(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,20}$")
