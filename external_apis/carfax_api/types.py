from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

from config import SOURCE


class ExternalUserIDSourceIn(BaseModel):
    user_external_id: str
    source: str = SOURCE

class Carfax(ExternalUserIDSourceIn):
    link: Optional[HttpUrl] = None
    is_paid: Optional[bool] = None
    vin: Optional[str] = None
    created_at: datetime
    id: int

class RequestCarfaxVin(ExternalUserIDSourceIn):
    vin: str