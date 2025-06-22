from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message

from database.crud.user import UserService
from telegram_bot.keyboards.murkup.admin import admin_keyboard

from aiogram.utils.i18n import gettext as _
admin = Router()

@admin.message(Command("admin"))
async def admin_command_handler(message: Message):
    telegram_id = message.from_user.id
    async with UserService() as db:
        user = await db.get_by_telegram_id(telegram_id)
        if user and user.is_admin:
            await message.answer(_('Use buttons below'), reply_markup=admin_keyboard())
        else:
            await message.answer(_('Access denied'))

