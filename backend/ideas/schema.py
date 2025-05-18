from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class IdeaBase(BaseModel):
    title: str
    description: str


class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class IdeaList(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseModel):
    username: str
    email: EmailStr
