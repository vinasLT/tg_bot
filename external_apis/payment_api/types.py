from pydantic import BaseModel, HttpUrl

from config import SOURCE


class StripeCheckOutIn(BaseModel):
    source: str = SOURCE
    external_user_id: str
    purpose: str = 'CARFAX'
    purpose_external_id: int
    success_link: str
    cancel_link: str

class StripeCheckOutOut(BaseModel):
    link: HttpUrl