from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    is_active: Optional[bool]


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
