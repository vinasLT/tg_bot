from functools import lru_cache
from typing import Union

from aiogram.types import Message, CallbackQuery
from httpx import HTTPStatusError
from pydantic import BaseModel

from auction_api.auction_api import AuctionApiClient
from auction_api.types import BasicLot, BasicHistoryLot, EndpointSchema
from aiogram.utils.i18n import gettext as _

def get_serialized_auction(base_site:str):
    return '🔴 IAAI' if base_site.lower() == 'iaai' else '🔵 COPART'

def serialize_lot(data: Union[BasicLot, BasicHistoryLot]) -> str:
    vehicle_name = f"{data.year if data.year else 'XXXX'} " \
                   f"{data.make.upper() if data.make else 'N/A'} " \
                   f"{data.model.upper() if data.model else 'N/A'} " \
                   f"{data.series.upper() if data.series else 'N/A'}"

    text = _(
        "<b>☑ {vehicle_name}</b>\n"
        "<b>☑ Lot ID:</b> <code>{lot_id}</code>\n"
        "<b>☑ VIN:</b> <code>{vin}</code>\n"
        "<b>☑ Auction:</b> {auction_name}\n"
        "<b>☑ Insurance:</b> {insurance}\n"
        "<b>☑ Title:</b> {title}\n\n"
        "<b>🔥 Current bid:</b> <b>${current_bid}</b>\n"
        "<b>🔥 Auction Status:</b> <b>{status}</b>\n"
        "<b>🔥 Auction Date:</b> <i>{auction_date}</i>\n"
    ).format(
        vehicle_name=vehicle_name,
        lot_id=data.lot_id,
        vin=data.vin,
        auction_name=get_serialized_auction(data.base_site),
        insurance='Yes' if data.seller_type == 'insurance' else 'No',
        title=data.document,
        current_bid=data.current_bid if data.current_bid is not None else 'N/A',
        status=data.form_get_type.upper() if data.form_get_type else 'N/A',
        auction_date=data.auction_date.strftime('%m/%d/%Y %H:%M'),
    )
    return text

def serialize_history(data: BasicHistoryLot) -> str:
    history = data.sale_history
    text = ''
    for num, i in enumerate(history):
        text += _(
            "<b>🔹 History #{num}</b>\n"
            "☑ <b>Lot ID:</b> <code>{lot_id}</code>\n"
            "☑ <b>Auction:</b> {auction}\n"
            "☑ <b>Date:</b> {date}\n"
            "☑ <b>Price:</b> ${price}\n"
            "☑ <b>Status:</b> <b>{status}</b>\n"
        ).format(
            num=num + 1,
            lot_id=i.lot_id,
            auction=get_serialized_auction(i.base_site),
            date=i.sale_date.strftime("%Y-%m-%d"),
            price=i.purchase_price if i.purchase_price is not None else 'N/A',
            status=i.sale_status.upper()
        )

        if num < len(history) - 1:
            text += "────────────────────────────\n"

    return text



def get_some_num_of_images(data: Union[BasicLot, BasicHistoryLot], num:int)-> list:
    if isinstance(data.link_img_hd, list):
        images = []
        for image in data.link_img_hd[:num]:
            images.append(str(image))
        return images
    return []

def generate_link_to_auction(lot_id: int, auction_name: str) -> str:
    if auction_name.lower() == 'copart':
        return f'https://www.copart.com/lot/{lot_id}'
    else:
        return f'https://www.iaai.com/Search?Keyword={lot_id}'




@lru_cache
def get_api_client()-> AuctionApiClient:
    return AuctionApiClient()


