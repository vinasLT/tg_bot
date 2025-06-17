from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('GET REPORT 🦊')),
                KeyboardButton(text=_('TRANSPORT COST CALC. 💸'))
            ],
            [
                KeyboardButton(text=_("CHECK LOT 🕵‍♂")),
                KeyboardButton(text=_("FIND FOR ME 🕵‍♂"))
            ],
            [
                KeyboardButton(text=_("HELP ✋")),
                KeyboardButton(text=_("LANGUAGE 🌍"))
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder=_("Select an action")
    )
