

from aiogram import Router, F
from aiogram.types import Message

from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from config import SECRET_ADMIN_KEY
from database.crud.find_for_me import FindForMeService
from database.crud.user import UserService
from database.schemas.find_for_me import FindForMeRead

from telegram_bot.keyboards.inline.find_for_me import new_find_for_me_request_received
from telegram_bot.utils.find_for_me import get_summary_text

admin_markup_router = Router()


@admin_markup_router.message(F.text == __('SEE ALL FIND FOR ME 🕵‍♂'))
async def respond_wait_for_lot_id(message: Message):
    async with UserService() as service:
        user = await service.get_by_telegram_id(message.from_user.id)
        if user and user.is_admin:
            async with FindForMeService() as find_for_me_service:
                all_active_requests = await find_for_me_service.get_all_active_requests()

                if not all_active_requests:
                    await message.answer("❌ No active requests found.")
                    return

                for active_request in all_active_requests:
                    pydantic_data = FindForMeRead.model_validate(active_request).model_dump()
                    text = get_summary_text(pydantic_data)
                    reply_markup = new_find_for_me_request_received(active_request.id)
                    await message.answer(text, reply_markup=reply_markup)


@admin_markup_router.message(F.text == __('ADD ADMIN ➕'))
async def add_admin(message: Message):
    from main import bot
    async with UserService() as service:
        user = await service.get_by_telegram_id(message.from_user.id)
        if user and user.is_admin:
            bot_info = await bot.get_me()
            bot_username = bot_info.username
            link = f"https://t.me/{bot_username}?start={SECRET_ADMIN_KEY}"

            await message.answer(
                _("Send this message to the user you want to promote:\n"
                  "Become admin - <a href='{link}'>click here</a>").format(link=link),
            )