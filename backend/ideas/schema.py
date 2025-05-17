from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class IdeaBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class IdeaList(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
