from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from app.db.models.users import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
