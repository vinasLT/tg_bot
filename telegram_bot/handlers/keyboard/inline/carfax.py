import httpx
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from external_apis.carfax_api.carfax_api import CarfaxAPI
from external_apis.carfax_api.serializers import serialize_carfax
from external_apis.carfax_api.types import ExternalUserIDSourceIn, RequestCarfaxVin
from external_apis.payment_api.payment_api import PaymentAPI
from external_apis.payment_api.types import StripeCheckOutIn

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
    async with CarfaxAPI() as api:
        get_all_carfaxes = await api.get_all_carfaxes(ExternalUserIDSourceIn(user_external_id=str(user_id)))
        if len(get_all_carfaxes) <= 0:
            await query.message.edit_text(_("❌ You don't have any purchased CarFax"))
            await query.answer()
        else:
            await query.answer()
            for carfax in get_all_carfaxes:
                text = serialize_carfax(carfax)
                await query.message.answer(text, reply_markup=buy_or_see(carfax))



@carfax_inline_router.callback_query(F.data.startswith('carfax_buy_'))
async def carfax_buy(query: CallbackQuery):
    from main import bot

    vin = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    await query.message.edit_text(_('🔄 Checking records...'), reply_markup=None)
    async with CarfaxAPI() as api:
        try:
            carfax = await api.get_carfax_by_vin(RequestCarfaxVin(user_external_id=str(user_id), vin=vin))
            print(carfax, 'BOUGHT')
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                carfax = await api.buy_carfax(RequestCarfaxVin(user_external_id=str(user_id), vin=vin))
            else:
                raise

    await query.message.edit_text(_('🔄 Retrieving checkout link...'))

    bot_info = await bot.get_me()
    bot_username = bot_info.username
    success_payment = f"https://t.me/{bot_username}?start=success_carfax_payment_{carfax.vin}"
    cancel_payment = f"https://t.me/{bot_username}"

    async with PaymentAPI() as api:
        link = await api.get_stripe_checkout(StripeCheckOutIn(external_user_id=str(user_id),
                                                                      purpose_external_id=carfax.id,
                                                                      success_link=success_payment,
                                                                      cancel_link=cancel_payment))
    await query.message.edit_text(_('Pay & Check below:'), reply_markup=payment_link(str(link.link), vin))

@carfax_inline_router.callback_query(F.data.startswith('check_payment_'))
async def check_payment(query: CallbackQuery):
    user_id = query.from_user.id
    vin = query.data.split('_')[-1]
    async with CarfaxAPI() as api:
        try:
            carfax = await api.get_carfax_by_vin(RequestCarfaxVin(user_external_id=str(user_id), vin=vin))
            if carfax.is_paid:
                await query.answer('☑️ Successfully paid!')
                text = serialize_carfax(carfax)
                await query.message.edit_text(text, reply_markup=buy_or_see(carfax))
                return
        except httpx.HTTPStatusError:
            pass
    await query.answer('❌ Not paid yet!')












