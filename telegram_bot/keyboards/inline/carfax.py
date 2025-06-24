from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

def carfax():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=_('🦊 See my CarFaxes'), callback_data=f'see_all_carfaxes'),
                    InlineKeyboardButton(text=_('💳 Buy new CarFax (2€)'), callback_data=f'buy_new_carfax')
                ]
            ]
)