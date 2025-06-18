import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from database.crud.user import UserService
from database.schemas.user import UserUpdate
from telegram_bot.keyboards.inline.choose_language import choose_language
from telegram_bot.keyboards.murkup.main_keyboard import start_keyboard
from telegram_bot.middelwares import i18n

choose_language_router = Router()

@choose_language_router.callback_query(F.data.startswith('choose_language_'))
async def choose_language_callback(query: CallbackQuery):
    data = query.data.split('_')
    language = data[-1]

    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(query.from_user.id)
        await user_service.update(user.id, UserUpdate(language=language))

    i18n.ctx_locale.set(language)

    await query.message.edit_reply_markup(reply_markup=choose_language(language))
    await query.answer()
    await query.message.answer(_('✅ Language successfully changed'), reply_markup=start_keyboard())

