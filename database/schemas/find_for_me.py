from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FindForMeBase(BaseModel):
    make: str
    model: str
    year_from: int
    year_to: int
    budget_from: str
    budget_to: str
    specific_message: Optional[str] = None
    user_id: int
    response_auction: Optional[str] = None
    response_lot_id: Optional[int] = None
    is_responded: Optional[bool] = None
    created_at: Optional[datetime] = None


class FindForMeCreate(FindForMeBase):
    pass


class FindForMeUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    budget_from: Optional[str] = None
    budget_to: Optional[str] = None
    specific_message: Optional[str] = None
    user_id: Optional[int] = None
    response_auction: Optional[str] = None
    response_lot_id: Optional[int] = None
    is_responded: Optional[bool] = False
    created_at: Optional[datetime] = None


class FindForMeRead(FindForMeBase):
    id: int

    class Config:
        from_attributes = True