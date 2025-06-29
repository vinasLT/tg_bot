from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from database.crud.user import UserService
from database.schemas.user import UserUpdate
from external_apis.auction_api.auction_api import AuctionAPI
from external_apis.auction_api.serializers import serialize_lot
from external_apis.auction_api.types import VINorLotIDIn
from database.crud.find_for_me import FindForMeService
from telegram_bot.keyboards.murkup.main_keyboard import start_keyboard
from telegram_bot.states.find_for_me import FindForMeStates
from telegram_bot.utils.callback_query import parse_callback_data
from telegram_bot.utils.find_for_me import get_summary_text, ask_confirmation, send_lot

request_phone_number_markup_router = Router()


@request_phone_number_markup_router.message(F.contact)
async def save_phone_number(message: Message):
    phone = message.contact.phone_number
    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(message.from_user.id)
        await user_service.update(user.id, UserUpdate(phone_number=phone))
    await message.answer(_('📱 Phone number saved successfully!'), reply_markup=start_keyboard())



