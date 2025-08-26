import grpc
import httpx
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from config import settings
from external_apis.carfax_api.serializers import serialize_carfax
from rpc_client.carfax_client import CarfaxRcpClient

from telegram_bot.keyboards.inline.carfax import buy_or_see, payment_link
from telegram_bot.states.carfax import CarfaxStates

carfax_inline_router = Router()

@carfax_inline_router.callback_query(F.data == 'buy_new_carfax')
async def buy_new_carfax(query: CallbackQuery, state: FSMContext):
    await query.message.answer(_('🚘 Enter the VIN of the vehicle for which you want to purchase a report:'))
    await state.set_state(CarfaxStates.wait_for_vin)
    await query.answer()

@carfax_inline_router.callback_query(F.data == 'see_all_carfaxes')
async def see_all_carfaxes(query: CallbackQuery):
    user_id = query.from_user.id
    async with CarfaxRcpClient() as rcp_client:
        try:
            get_all_carfaxes = await rcp_client.get_all_carfaxes_for_user(user_external_id=str(user_id), source=settings.SOURCE)
            all_carfaxes = get_all_carfaxes.carfax
        except grpc.aio.AioRpcError as e:
            print(e.code())
            print(e.details())
            all_carfaxes = []

        if len(all_carfaxes) <= 0:
            await query.message.edit_text(_("❌ You don't have any purchased CarFax"))
            await query.answer()
        else:
            await query.answer()
            for carfax in all_carfaxes:
                text = serialize_carfax(carfax)
                await query.message.answer(text, reply_markup=buy_or_see(carfax))


@carfax_inline_router.callback_query(F.data.startswith('carfax_buy_'))
async def carfax_buy(query: CallbackQuery):
    from main import bot

    vin = query.data.split('_')[-1]
    user_id = query.from_user.id

    #
    #
    #
    #     try:
    #         response = await rcp_client.get_carfax_by_vin(user_external_id=str(user_id), vin=vin,
    #                                                       source=settings.SOURCE)
    #         carfax = response.carfax
    #
    #     except grpc.aio.AioRpcError as e:
    #         if e.code() == grpc.StatusCode.NOT_FOUND:
    #            response = None
    #         else:
    #             await query.message.edit_text(_('❌ Something went wrong, please try again later'))
    #             return
    #



    bot_info = await bot.get_me()
    bot_username = bot_info.username
    success_payment = f"https://t.me/{bot_username}?start=success_carfax_payment_{vin}"
    cancel_payment = f"https://t.me/{bot_username}"
    await query.message.edit_text(_('🔄 Checking records...'), reply_markup=None)
    async with CarfaxRcpClient() as rcp_client:
        try:
            response = await rcp_client.buy_carfax(user_external_id=str(user_id), vin=vin,
                                               source=settings.SOURCE, cancel_url=cancel_payment,
                                               success_url=success_payment)
            checkout_link = response.link
            await query.message.edit_text(_('Pay & Check below:'), reply_markup=payment_link(checkout_link, vin))
        except grpc.aio.AioRpcError as e:
            await query.message.edit_text(_('❌ Failed to create payment link, please try again later'))
    await query.answer()

@carfax_inline_router.callback_query(F.data.startswith('check_payment_'))
async def check_payment(query: CallbackQuery):
    user_id = query.from_user.id
    vin = query.data.split('_')[-1]
    async with CarfaxRcpClient() as rcp_client:
        try:
            response = await rcp_client.get_carfax_by_vin(user_external_id=str(user_id), vin=vin, source=settings.SOURCE)
            carfax = response.carfax
            if carfax.is_paid:
                await query.answer('☑️ Successfully paid!')
                text = serialize_carfax(carfax)
                await query.message.edit_text(text, reply_markup=buy_or_see(carfax))
                return
        except httpx.HTTPStatusError:
            pass
    await query.answer('❌ Not paid yet!')












