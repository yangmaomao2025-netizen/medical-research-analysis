"""
用户认证相关模型
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    username: str
    real_name: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    hospital: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    hospital: Optional[str] = None
    research_areas: Optional[list] = None
    disease_spectrum: Optional[list] = None

class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    avatar: Optional[str] = None
    orcid: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
