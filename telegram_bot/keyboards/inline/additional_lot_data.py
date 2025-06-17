from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from auction_api.utils import generate_link_to_auction


def lot_inline_keyboard(vin: str, lot_id:int, auction_name:str):
    lot_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('📊 Sales statistics'), callback_data=f'sales_statistics_{vin}_{auction_name}')
            ],
            [
                InlineKeyboardButton(text=_('ℹ️ About the car'), callback_data=f'about_car_{vin}_{auction_name}')
            ],
            [
                InlineKeyboardButton(text=_('🖼 More Photos'), callback_data=f'more_photos_{lot_id}_{auction_name}')
            ],
            [
                InlineKeyboardButton(text=_('🔗 Open auction'), url=generate_link_to_auction(lot_id, auction_name)),
            ],
        ]
    )
    return lot_inline