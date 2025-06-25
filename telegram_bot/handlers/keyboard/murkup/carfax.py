import re
from multiprocessing.reduction import steal_handle

import httpx
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from external_apis.auction_api.auction_api import AuctionAPI
from external_apis.auction_api.types import VINorLotIDIn
from database.crud.find_for_me import FindForMeService
from database.crud.user import UserService
from external_apis.carfax_api.carfax_api import CarfaxAPI
from external_apis.carfax_api.serializers import serialize_carfax
from external_apis.carfax_api.types import RequestCarfaxVin
from telegram_bot.handlers.keyboard.inline.find_for_me import ask_confirmation
from telegram_bot.keyboards.inline.carfax import buy_or_cancel, buy_or_see
from telegram_bot.keyboards.inline.find_for_me import find_for_me_start_cancel, skip_keyboard, choose_auction
from telegram_bot.states.carfax import CarfaxStates
from telegram_bot.states.find_for_me import FindForMeStates
from telegram_bot.utils.find_for_me import send_lot

carfax_markup_router = Router()


@carfax_markup_router.message(CarfaxStates.wait_for_vin)
async def respond_wait_for_lot_id(message: Message, state: FSMContext):
    vin_raw = message.text.upper()
    vin_cleaned = re.sub(r'[^A-Z0-9]', '', vin_raw)

    user_id = message.from_user.id

    if not vin_cleaned:
        await message.answer(_('❌ You entered an invalid VIN number, try again'))
        return
    async with AuctionAPI() as api:
        try:
            response = await api.get_lot_by_vin_or_id(VINorLotIDIn(vin_or_lot=vin_cleaned))
        except (httpx.TransportError, httpx.HTTPStatusError):
            response = None

    if not response:
        await message.answer(_('❌ You entered an invalid VIN number, try again'))
        return
    async with CarfaxAPI() as api:
        try:
            carfax = await api.get_carfax_by_vin(RequestCarfaxVin(user_external_id=str(user_id), vin=vin_cleaned))
            text = serialize_carfax(carfax)
            await message.answer(text, reply_markup=buy_or_see(carfax))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                await message.answer(_('Check again, is this the correct VIN code?\n'
                                       'VIN: <b>{vin}</b>').format(vin=vin_cleaned), reply_markup=buy_or_cancel(vin_cleaned))
    await state.clear()
