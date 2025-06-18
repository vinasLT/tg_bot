from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSearchHistoryBase(BaseModel):
    lot_id: int
    auction_name: str
    user_id: int
    created_at: Optional[datetime] = None



class UserSearchHistoryCreate(UserSearchHistoryBase):
    pass


class UserSearchHistoryUpdate(UserSearchHistoryBase):
    pass


class UserSearchHistoryRead(UserSearchHistoryBase):
    id: int

    class Config:
        from_attributes = True