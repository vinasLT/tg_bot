from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from telegram_bot.keyboards.inline.cancel import cancel_button
#USER
def find_for_me_start_cancel():
    lot_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('☑️ Start'), callback_data=f'start_find_for_me'),
                cancel_button()
            ],

        ]
    )
    return lot_inline

def confirm_keyboard(callback_date: str = "confirm_find_for_me"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("✅ Send"), callback_data=callback_date),
                cancel_button()
            ],

        ]
    )

def skip_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("⏭ Skip"), callback_data="skip_specific_message")]
        ]
    )

#ADMIN
def new_find_for_me_request_received(request_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('✍️ Respond'), callback_data=f'respond_find_request_{request_id}'),
            ]
        ]
    )


def choose_auction(lot_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔴 IAAI', callback_data=f'find_for_me_choose_auction_{lot_id}_iaai'),
                InlineKeyboardButton(text='🔵 COPART', callback_data=f'find_for_me_choose_auction_{lot_id}_copart'),
            ]
        ]
    )

