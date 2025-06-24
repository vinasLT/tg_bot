from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from external_apis.auction_api import BasicLot

def choose_one_lot(lots: List[BasicLot]) -> InlineKeyboardMarkup:
    buttons: List[InlineKeyboardButton] = []
    for num, lot in enumerate(lots):
        buttons.append(InlineKeyboardButton(text=f'#{num+1}', callback_data=f'open_lot_{lot.lot_id}_{lot.base_site}'))

    choose_button = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons
        ]
    )
    return choose_button