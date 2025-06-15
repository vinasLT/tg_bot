from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Get report 🦊')),
                KeyboardButton(text=_('Transport cost calc. 💵'))
            ],
            [
                KeyboardButton(text=_("Check lot 🚗")),
                KeyboardButton(text=_("Find My 🔍"))
            ],
            [
                KeyboardButton(text=_("Help ✋")),
                KeyboardButton(text=_("Language 🌎"))
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder=_("Select an action")
    )
