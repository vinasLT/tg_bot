from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from database.crud.user import UserService
from database.schemas.user import UserUpdate, UserCreate
from telegram_bot.keyboards.murkup.start import start_keyboard

from aiogram.utils.i18n import gettext as _
start = Router()

@start.message(CommandStart())
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    async with UserService() as db:
        user = await db.get_by_telegram_id(telegram_id)

        start_message = _('Hello! We not only help you save up to 50% when purchasing a vehicle from the USA,\n'
                                     'but we also ensure that the process is completely safe, transparent, and without any hidden details! \n'
                                     'Join our rapidly growing group where youll be the first to see the hottest offers: \n'
                                     '<a href="https://www.facebook.com/groups/417661698833379/" target="_blank">click here to join</a>.')
        if user:
            await db.update(user.id, UserUpdate(language='en'))
            if user.is_admin:
                await message.answer(_('Hi, you admin, you can access admin panel'))
            else:
                await message.answer(start_message, reply_markup=start_keyboard())
        else:
            await db.create(UserCreate(telegram_id=telegram_id, language='en'))
            await message.answer(start_message, reply_markup=start_keyboard())
