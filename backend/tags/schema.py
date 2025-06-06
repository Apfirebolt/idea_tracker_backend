from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class TagBase(BaseModel):
    name: str
    description: str


class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AddTag(BaseModel):
    tags: List[str]


class TagList(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseModel):
    username: str
    email: EmailStr
