from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    language: Optional[str] = 'en'
    is_admin: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    language: Optional[str] = None
    is_admin: Optional[bool] = False


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
