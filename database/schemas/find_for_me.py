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
    created_at: Optional[datetime] = None


class FindForMeCreate(FindForMeBase):
    pass


class FindForMeUpdate(FindForMeBase):
    pass


class FindForMeRead(FindForMeBase):
    id: int

    class Config:
        from_attributes = True