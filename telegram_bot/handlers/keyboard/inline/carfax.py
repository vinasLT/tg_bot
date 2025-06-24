from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from database.crud.user import UserService
from database.schemas.user import UserUpdate
from telegram_bot.keyboards.inline.choose_language import choose_language
from telegram_bot.keyboards.murkup.main_keyboard import start_keyboard
from telegram_bot.middelwares import i18n

carfax_inline_router = Router()

@carfax_inline_router.callback_query(F.data == 'buy_new_carfax')
async def buy_new_carfax(query: CallbackQuery):
    pass

@carfax_inline_router.callback_query(F.data == 'see_all_carfaxes')
async def see_all_carfaxes(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id








