from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _



def choose_language(current_language: str):
    languages = [
        ('en', _('English 🇺🇸')),
        ('lt', _('Lithuanian 🇱🇹')),
        ('ee', _('Estonian 🇪🇪')),
        ('pl', _('Polish 🇵🇱')),
        ('lv', _('Latvian 🇱🇻')),
        ('ru', _('Russian 🇷🇺')),
    ]

    keyboard = []

    for code, name in languages:
        mark = '✅ ' if current_language == code else ''
        keyboard.append([
            InlineKeyboardButton(text=f"{mark}{name}", callback_data=f'choose_language_{code}')
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)