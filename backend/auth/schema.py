from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic import ValidationError, field_validator


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


    @field_validator('username')
    @classmethod
    def username_min_length(cls, v):
        if len(v) < 4:
            raise ValueError('Username must be at least 4 characters long')
        return v
    
    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    

    model_config = ConfigDict(from_attributes=True)

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
