from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from rpc_client.gen.python.auction.v1 import lot_pb2


def choose_one_lot(lots: List[lot_pb2.Lot]) -> InlineKeyboardMarkup:
    buttons: List[InlineKeyboardButton] = []
    for num, lot in enumerate(lots):
        buttons.append(InlineKeyboardButton(text=f'#{num+1}', callback_data=f'open_lot_{lot.lot_id}_{lot.base_site}'))

    choose_button = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons
        ]
    )
    return choose_button