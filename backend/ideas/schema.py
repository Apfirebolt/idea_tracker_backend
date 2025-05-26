from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from backend.tags.schema import TagList, TagBase
from backend.scripts.schema import ScriptBase


class IdeaBase(BaseModel):
    title: str
    description: str
    tags: Optional[list[str]] = None


class IdeaCreateResponse(BaseModel):
    title: str
    description: str

    tags: Optional[list[TagList]] = None


class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = None


class IdeaList(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    status: Optional[str] = None
    is_shared: Optional[int]
    created_at: datetime
    updated_at: datetime

    tags: Optional[list[TagBase]] = None
    scripts: Optional[list[ScriptBase]] = None


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class IdeaItemSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    tags: Optional[list[TagBase]] = None


class PaginatedIdeaList(BaseModel):
    items: list[IdeaItemSchema]
    total: int
    page: int
    size: int
    pages: int
