from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from database.crud.user import UserService
from database.schemas.user import UserUpdate
from telegram_bot.keyboards.murkup.main_keyboard import start_keyboard

request_phone_number_markup_router = Router()

@request_phone_number_markup_router.message(F.contact)
async def save_phone_number(message: Message):
    phone = message.contact.phone_number
    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(message.from_user.id)
        await user_service.update(user.id, UserUpdate(phone_number=phone))
    await message.answer(_('📱 Phone number saved successfully!'), reply_markup=start_keyboard())



