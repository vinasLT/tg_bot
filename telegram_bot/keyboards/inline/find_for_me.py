from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from telegram_bot.keyboards.inline.cancel import cancel_button

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

def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("✅ Send"), callback_data="confirm_find_for_me"),
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