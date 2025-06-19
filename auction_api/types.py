from datetime import datetime
from typing import Literal, Type, Optional, List, Union

from pydantic import BaseModel, HttpUrl, Field, PositiveInt


class EndpointSchema(BaseModel):
    validation_schema: Type[BaseModel]
    endpoint:str
    method: Literal['GET', 'POST']
    out_schema_default: Type[BaseModel]
    out_schema_history: Optional[Type[BaseModel]] = None
    is_list: bool = False

class BasicLot(BaseModel):
    lot_id: int
    site: int
    base_site: str
    salvage_id: Optional[int]
    odometer: Optional[int]
    price_new: Optional[int]
    price_future: Optional[int]
    reserve_price: Optional[int]
    current_bid: Optional[int] = Field(0)
    auction_date: Optional[datetime] = Field(None)
    cost_priced: Optional[int]
    cost_repair: Optional[int]
    year: Optional[int]
    cylinders: Optional[int]
    state: Optional[str]
    vehicle_type: Optional[str]
    auction_type: Optional[str]
    make: Optional[str]
    model: Optional[str]
    series: Optional[str]
    damage_pr: Optional[str]
    damage_sec: Optional[str]
    keys: Optional[str]
    odobrand: Optional[str]
    fuel: Optional[str]
    drive: Optional[str]
    transmission: Optional[str]
    color: Optional[str]
    status: Optional[str]
    title: Optional[str]
    vin: Optional[str]
    engine: Optional[str]
    engine_size: Optional[float]
    location: Optional[str]
    location_old: Optional[str]
    location_id: Optional[int]
    country: Optional[str]
    document: Optional[str]
    document_old: Optional[str]
    currency: Optional[str]
    seller: Optional[str]
    is_buynow: bool
    iaai_360: Optional[str]
    copart_exterior_360: List[str]
    copart_interior_360: Optional[str]
    video: Optional[str]
    link_img_hd: List[HttpUrl]
    link_img_small: List[HttpUrl]
    is_offsite: bool
    location_offsite: Optional[str]
    link: HttpUrl
    body_type: Optional[str] = Field(None)
    seller_type: Optional[str]
    vehicle_score: Optional[str]
    form_get_type: str = Field(default='history')


class SaleHistoryItem(BaseModel):
    lot_id: int
    site: int
    base_site: str
    vin: str
    sale_status: Optional[str] = None
    sale_date: Optional[datetime] = None
    purchase_price: Optional[int]
    is_buynow: bool
    buyer_state: Optional[str]
    buyer_country: Optional[str]
    vehicle_type: Optional[str]

class BasicHistoryLot(BasicLot):
    sale_history: Optional[List[SaleHistoryItem]] = None
    sale_date: Optional[datetime] = None
    sale_status: Optional[str] = None
    purchase_price: Optional[int] = None

class LotByIDIn(BaseModel):
    lot_id: PositiveInt
    site: Optional[Union[int, str]]

class LotByVINIn(BaseModel):
    vin: str
    site: Optional[Union[int, str]]

class CurrentBidOut(BaseModel):
    pre_bid: PositiveInt

class VINorLotIDIn(BaseModel):
    vin_or_lot: str
    site: Optional[Union[int, str]] = Field(default=None)


class ChooseLot(LotByIDIn):
    site: Union[int, str]