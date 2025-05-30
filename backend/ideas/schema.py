from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from backend.tags.schema import TagList, TagBase
from backend.scripts.schema import ScriptBase
from backend.auth.schema import DisplayAccount


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
    is_shared: Optional[int] = 0


class IdeaCommentSchema(BaseModel):
    id: int
    content: str
    created_at: datetime

class IdeaComment(BaseModel):
    id: int
    content: str
    idea_id: int
    user_id: Optional[int] = None
    created_at: datetime
    user: Optional[DisplayAccount] = None

    class Config:
        from_attributes = True


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
    comments: Optional[list[IdeaComment]] = None

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class AddIdeaComment(BaseModel):
    content: str
    idea_id: int


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


class IdeaImageSchema(BaseModel):
    id: int
    idea_id: int
    cloudinary_url: str = Field(..., alias="cloudinary_url") # Explicitly map if needed
    image_name: str
    image_type: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
