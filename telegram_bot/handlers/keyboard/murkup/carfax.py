import re

import grpc
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from config import settings
from external_apis.carfax_api.serializers import serialize_carfax
from rpc_client.carfax_client import CarfaxRcpClient
from telegram_bot.keyboards.inline.carfax import buy_or_cancel, buy_or_see
from telegram_bot.states.carfax import CarfaxStates

carfax_markup_router = Router()


@carfax_markup_router.message(CarfaxStates.wait_for_vin)
async def respond_wait_for_lot_id(message: Message, state: FSMContext):
    vin_raw = message.text.upper()
    vin_cleaned = re.sub(r'[^A-Z0-9]', '', vin_raw)

    user_id = message.from_user.id

    if not vin_cleaned:
        await message.answer(_('❌ You entered an invalid VIN number, try again'))
        return


    async with CarfaxRcpClient() as rpc_client:
        try:
            is_vin_exists = await rpc_client.is_vin_exists(vin=vin_cleaned)
        except grpc.aio.AioRpcError as e:
            details = e.details()
            await message.answer(_('❌ You entered an invalid VIN number, try again\n'
                                   'Error: {details}').format(details=details))

        if not is_vin_exists.is_exists:
            await message.answer(_('❌ You entered an invalid VIN number, try again'))
            return

        try:
            carfax = await rpc_client.get_carfax_by_vin(vin=vin_cleaned, user_external_id=str(user_id), source=settings.SOURCE)
            text = serialize_carfax(carfax.carfax)
            await message.answer(text, reply_markup=buy_or_see(carfax.carfax))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                await message.answer(_('Check again, is this the correct VIN code?\n'
                                       'VIN: <b>{vin}</b>').format(vin=vin_cleaned), reply_markup=buy_or_cancel(vin_cleaned))
    await state.clear()
