from aiogram.filters import CommandStart, CommandObject
from aiogram import Router
from aiogram.types import Message

from config import SECRET_ADMIN_KEY
from database.crud.user import UserService
from database.schemas.user import UserUpdate, UserCreate
from external_apis.carfax_api.carfax_api import CarfaxAPI
from external_apis.carfax_api.serializers import serialize_carfax
from external_apis.carfax_api.types import RequestCarfaxVin
from telegram_bot.keyboards.inline.carfax import buy_or_see
from telegram_bot.keyboards.murkup.main_keyboard import start_keyboard

from aiogram.utils.i18n import gettext as _
start = Router()

@start.message(CommandStart())
async def start_handler(message: Message, command: CommandObject):
    telegram_id = message.from_user.id
    username = message.from_user.username
    args = command.args
    if args and args.startswith('success_carfax_payment_'):
        vin = args.split('_')[-1]
        async with CarfaxAPI() as api:
            carfax = await api.get_carfax_by_vin(RequestCarfaxVin(user_external_id=str(telegram_id), vin=vin))
            text = serialize_carfax(carfax)
            await message.answer(text, reply_markup=buy_or_see(carfax))
        return

    async with UserService() as db:
        user = await db.get_by_telegram_id(telegram_id)

        start_message = _(
            "<b>👋 Hello!</b>\n\n"
            "🚗 We help you <b>save up to 50%</b> when purchasing a vehicle from the USA.\n"
            "🛡️ The entire process is <b>safe, transparent</b> and free from hidden details.\n\n"
            "🔥 <b>Join our fast-growing community</b> to be the first to see the hottest offers:\n"
            '<a href="https://www.facebook.com/groups/417661698833379/" target="_blank">👉 Click here to join the group</a>'
        )

        if user:
            if args and args == SECRET_ADMIN_KEY and not user.is_admin:
                await db.update(user.id, UserUpdate(is_admin=True))
                await message.answer(_('Hi, you are now admin! Access admin panel using this command - /admin'), reply_markup=start_keyboard())
            else:
                await message.answer(
                    _('Hi, you admin, you can access admin panel using this command - /admin') if user.is_admin else start_message,
                    reply_markup=start_keyboard()
                )
        else:
            is_admin = args == SECRET_ADMIN_KEY
            await db.create(UserCreate(telegram_id=telegram_id, language='en', is_admin=is_admin, username=username))

            if is_admin:
                await message.answer(_('Hi, you are now admin! Access admin panel using this command - /admin'), reply_markup=start_keyboard())
            else:
                await message.answer(start_message, reply_markup=start_keyboard())
