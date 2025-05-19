from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from backend.tags.schema import TagList


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

    tags: Optional[list[TagList]] = None


class UserSchema(BaseModel):
    username: str
    email: EmailStr
