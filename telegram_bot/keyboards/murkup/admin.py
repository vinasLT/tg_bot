from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('SEE ALL FIND FOR ME 🕵‍♂')),
            ],
            [
                KeyboardButton(text=_('ADD ADMIN ➕')),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder=_("Select an action")
    )
