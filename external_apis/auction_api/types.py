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
    lot_id: Optional[int] = None
    site: Optional[int] = None
    base_site: Optional[str] = None
    salvage_id: Optional[int] = None
    odometer: Optional[int] = None
    price_new: Optional[int] = None
    price_future: Optional[int] = None
    reserve_price: Optional[int] = None
    current_bid: Optional[int] = None
    auction_date: Optional[datetime] = None
    cost_priced: Optional[int] = None
    cost_repair: Optional[int] = None
    year: Optional[int] = None
    cylinders: Optional[int] = None
    state: Optional[str] = None
    vehicle_type: Optional[str] = None
    auction_type: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    series: Optional[str] = None
    damage_pr: Optional[str] = None
    damage_sec: Optional[str] = None
    keys: Optional[str] = None
    odobrand: Optional[str] = None
    fuel: Optional[str] = None
    drive: Optional[str] = None
    transmission: Optional[str] = None
    color: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    vin: Optional[str] = None
    engine: Optional[str] = None
    engine_size: Optional[float] = None
    location: Optional[str] = None
    location_old: Optional[str] = None
    location_id: Optional[int] = None
    country: Optional[str] = None
    document: Optional[str] = None
    document_old: Optional[str] = None
    currency: Optional[str] = None
    seller: Optional[str] = None
    is_buynow: Optional[bool] = None
    iaai_360: Optional[str] = None
    copart_exterior_360: Optional[List[str]] = None
    copart_interior_360: Optional[str] = None
    video: Optional[str] = None
    link_img_hd: Optional[List[HttpUrl]] = None
    link_img_small: Optional[List[HttpUrl]] = None
    is_offsite: Optional[bool] = None
    location_offsite: Optional[str] = None
    link: Optional[HttpUrl] = None
    body_type: Optional[str] = None
    seller_type: Optional[str] = None
    vehicle_score: Optional[str] = None
    form_get_type: str = Field(default='history')


class SaleHistoryItem(BaseModel):
    lot_id: Optional[int] = None
    site: Optional[int] = None
    base_site: Optional[str] = None
    vin: Optional[str] = None
    sale_status: Optional[str] = None
    sale_date: Optional[datetime] = None
    purchase_price: Optional[int] = None
    is_buynow: Optional[bool] = None
    buyer_state: Optional[str] = None
    buyer_country: Optional[str] = None
    vehicle_type: Optional[str] = None

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