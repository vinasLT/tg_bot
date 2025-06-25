from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from external_apis.auction_api.auction_api import AuctionAPI
from external_apis.auction_api.types import VINorLotIDIn
from database.crud.find_for_me import FindForMeService
from database.crud.user import UserService
from telegram_bot.handlers.keyboard.inline.find_for_me import ask_confirmation
from telegram_bot.keyboards.inline.find_for_me import find_for_me_start_cancel, skip_keyboard, choose_auction
from telegram_bot.states.find_for_me import FindForMeStates
from telegram_bot.utils.find_for_me import send_lot

find_for_me_markup_router = Router()


@find_for_me_markup_router.message(FindForMeStates.wait_for_lot_id)
async def respond_wait_for_lot_id(message: Message):
    vin_or_lot_id = message.text
    loading_message = await message.answer(_('⏳ Loading...'))

    async with AuctionAPI() as api:
        response = await api.get_lot_by_vin_or_id(VINorLotIDIn(vin_or_lot=vin_or_lot_id))

        if len(response) == 1:
            item = response[0]
            await send_lot(loading_message, item)
        else:
            await message.answer(_('We found two lots with same lot ID, choose auction:'), reply_markup=choose_auction(response[0].lot_id))


@find_for_me_markup_router.message(F.text == __('FIND FOR ME 🕵‍♂'))
async def find_for_me(message: Message):
    async with UserService() as user_service:
        async with FindForMeService() as find_for_me_service:
            user = await user_service.get_by_telegram_id(message.from_user.id)
            if await find_for_me_service.is_user_have_unresponded_requests(user.id):
                await message.answer(_("You have already submitted a 'Find for me' request."
                                       " Please wait for a response — once we reply, you'll be able to send a new request."))
                return


        await message.answer(_('🔍 <b>How "Find for Me" works:</b>\n'
                               '<b>1.</b> You fill out a short form with:\n'
                               '– <b>Make</b>\n'
                               '– <b>Model</b>\n'
                               '– <b>Year</b>\n'
                               '– <b>Budget</b>\n'
                               '<b>2.</b> Our team searches for matching vehicles.\n'
                               '<b>3.</b> If you like the suggestion, <b>we help you buy and ship it!</b>'),
                             reply_markup=find_for_me_start_cancel())


@find_for_me_markup_router.message(FindForMeStates.wait_for_make)
async def process_make(message: Message, state: FSMContext):
    make = message.text.strip()
    if not make.isalpha():
        await message.answer(_('❌ Make must contain only letters. Try again:'))
        return
    await state.update_data(make=make)
    await message.answer(_('📦 Write the model:'))
    await state.set_state(FindForMeStates.wait_for_model)


@find_for_me_markup_router.message(FindForMeStates.wait_for_model)
async def process_model(message: Message, state: FSMContext):
    model = message.text.strip()
    if not model or not any(char.isalnum() for char in model):
        await message.answer(_('❌ Model must contain letters or numbers. Try again:'))
        return
    await state.update_data(model=model)
    await message.answer(_('📅 Year from (e.g. 2015):'))
    await state.set_state(FindForMeStates.wait_for_year_from)


@find_for_me_markup_router.message(FindForMeStates.wait_for_year_from)
async def process_year_from(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1900 <= int(message.text) <= 2050):
        await message.answer(_('❌ Invalid year. Enter a number like 2015:'))
        return
    await state.update_data(year_from=int(message.text))
    await message.answer(_('📅 Year to (e.g. 2020):'))
    await state.set_state(FindForMeStates.wait_for_year_to)


@find_for_me_markup_router.message(FindForMeStates.wait_for_year_to)
async def process_year_to(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1900 <= int(message.text) <= 2050):
        await message.answer(_('❌ Invalid year. Enter a number like 2020:'))
        return
    await state.update_data(year_to=int(message.text))
    await message.answer(_('💰 Budget from (USD):'))
    await state.set_state(FindForMeStates.wait_for_budget_from)


@find_for_me_markup_router.message(FindForMeStates.wait_for_budget_from)
async def process_budget_from(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(_('❌ Budget must be a number. Try again:'))
        return
    await state.update_data(budget_from=message.text)
    await message.answer(_('💰 Budget to (USD):'))
    await state.set_state(FindForMeStates.wait_for_budget_to)


@find_for_me_markup_router.message(FindForMeStates.wait_for_budget_to)
async def process_budget_to(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(_('❌ Budget must be a number. Try again:'))
        return

    await state.update_data(budget_to=message.text)
    await message.answer(_('📝 Want to tell us anything specific?\nDescribe it or press skip:'), reply_markup=skip_keyboard())
    await state.set_state(FindForMeStates.wait_for_specific_message)

@find_for_me_markup_router.message(FindForMeStates.wait_for_specific_message)
async def process_specific_message(message: Message, state: FSMContext):
    await state.update_data(specific_message=message.text.strip())
    await ask_confirmation(message, state)