from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from backend.ideas.schema import IdeaList


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class DisplayAccount(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    email: str
    role: str


class TokenData(BaseModel):
    email: Optional[str] = None
    id: Optional[int]
