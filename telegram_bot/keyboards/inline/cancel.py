from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

def cancel_button():
    return InlineKeyboardButton(text=_('Cancel ❌'), callback_data=f'cancel')

def cancel_keyboard():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    cancel_button(),
                ]
            ]
    )