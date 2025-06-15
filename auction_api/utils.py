from functools import lru_cache
from typing import Union

from auction_api.auction_api import AuctionApiClient
from auction_api.types import BasicLot, BasicHistoryLot
from aiogram.utils.i18n import gettext as _


def serialize_lot(data: Union[BasicLot, BasicHistoryLot]) -> str:
    text = _('🚘 {vehicle_name}\n'
            '🆔 Lot ID: {lot_id}\n'
            '📝 VIN: {vin}\n'
            '{insurance_emoji} Insurance: {insurance}\n'
            '📄 Title: {title}\n\n'
            '💵 Current bid: ${current_bid}\n'
            '📊 Auction Status: {status}\n'
            '🗓 Auction Date: {auction_date}\n'
            ).format(vehicle_name=f'{data.year if data.year else "XXXX"} {data.make.upper() if data.make else "N/A"} '
                                    f'{data.model.upper() if data.model else "N/A"} '
                                    f'{data.series.upper() if data.series else "N/A"}',
                       lot_id=data.lot_id,
                       vin=data.vin,
                       insurance_emoji='✅' if data.seller_type == 'insurance' else '⛔️',
                       insurance='Yes' if data.seller_type == 'insurance' else 'No',
                       title=data.document,
                       current_bid=data.current_bid if data.current_bid is not None else 'N/A',
                       status=data.form_get_type.upper() if data.form_get_type else 'N/A',
                       auction_date=data.auction_date.strftime('%m/%d/%Y %H:%M'),
                       )
    return text

def get_first_3_images(data: Union[BasicLot, BasicHistoryLot]):
    images = []
    for image in data.link_img_hd[:3]:
        images.append(str(image))
    return images

@lru_cache
def get_api_client():
    return AuctionApiClient()


