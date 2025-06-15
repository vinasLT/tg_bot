from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.keyboards.inline.cancel import cancel_button


def choose_auction(vin_or_lot_id: str):
    lot_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔵 COPART', callback_data=f'choose_copart_{vin_or_lot_id}')
            ],
            [
                InlineKeyboardButton(text='🔴 IAAI', callback_data=f'choose_iaai_{vin_or_lot_id}')
            ],
            [
                cancel_button()
            ]

        ]
    )
    return lot_inline