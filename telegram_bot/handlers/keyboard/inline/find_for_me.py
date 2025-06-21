from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from database.crud.find_for_me import FindForMeService
from database.crud.user import UserService
from database.schemas.find_for_me import FindForMeCreate
from telegram_bot.handlers.keyboard.murkup.find_for_me import find_for_me_router
from telegram_bot.keyboards.inline.cancel import cancel_keyboard
from telegram_bot.keyboards.inline.find_for_me import confirm_keyboard, skip_keyboard
from telegram_bot.states.find_for_me import FindForMeStates

find_for_me_inline_router = Router()

async def ask_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()

    summary = _(
        "<b>🚘 Make:</b> {make}\n"
        "<b>📦 Model:</b> {model}\n"
        "<b>📅 Year From:</b> {year_from}\n"
        "<b>📅 Year To:</b> {year_to}\n"
        "<b>💰 Budget From:</b> {budget_from}$\n"
        "<b>💰 Budget To:</b> {budget_to}$\n"
    ).format(year_to=data.get('year_to'), make=data.get('make'), year_from=data.get('year_from'),
                                                 model=data.get('model'), budget_from=data.get('budget_from'), budget_to=data.get('budget_to'))

    if data.get("specific_message"):
        summary += _("<b>📝 Note:</b> {specific_message}\n").format(specific_message=data["specific_message"])

    summary += _("\n✅ Do you want to send this request?")

    await message.answer(summary, reply_markup=confirm_keyboard())
    await state.set_state(FindForMeStates.wait_for_confirmation)


@find_for_me_inline_router.callback_query(F.data == 'start_find_for_me')
async def start_find_for_me(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(_('🚘 Write the make:'), reply_markup=cancel_keyboard())
    await state.set_state(FindForMeStates.wait_for_make)
    await query.answer()

@find_for_me_router.callback_query(F.data == "confirm_find_for_me")
async def confirm_send(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(query.from_user.id)
        async with FindForMeService() as service:
            await service.create(FindForMeCreate(year_to=data.get('year_to'), make=data.get('make'), year_from=data.get('year_from'),
                                                 model=data.get('model'), budget_from=data.get('budget_from'), budget_to=data.get('budget_to'), specific_message=data.get('specific_message'), user_id=user.id))

    await query.message.edit_text(_('✅ Your request has been saved!'))
    await state.clear()
    await query.answer()

@find_for_me_router.callback_query(F.data == "skip_specific_message")
async def skip_specific_message(query: CallbackQuery, state: FSMContext):
    await state.update_data(specific_message=None)
    await ask_confirmation(query.message, state)
    await query.answer()


@find_for_me_router.message(FindForMeStates.wait_for_make)
async def process_make(message: Message, state: FSMContext):
    make = message.text.strip()
    if not make.isalpha():
        await message.answer(_('❌ Make must contain only letters. Try again:'))
        return
    await state.update_data(make=make)
    await message.answer(_('📦 Write the model:'))
    await state.set_state(FindForMeStates.wait_for_model)


@find_for_me_router.message(FindForMeStates.wait_for_model)
async def process_model(message: Message, state: FSMContext):
    model = message.text.strip()
    if not model or not any(char.isalnum() for char in model):
        await message.answer(_('❌ Model must contain letters or numbers. Try again:'))
        return
    await state.update_data(model=model)
    await message.answer(_('📅 Year from (e.g. 2015):'))
    await state.set_state(FindForMeStates.wait_for_year_from)


@find_for_me_router.message(FindForMeStates.wait_for_year_from)
async def process_year_from(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1900 <= int(message.text) <= 2050):
        await message.answer(_('❌ Invalid year. Enter a number like 2015:'))
        return
    await state.update_data(year_from=int(message.text))
    await message.answer(_('📅 Year to (e.g. 2020):'))
    await state.set_state(FindForMeStates.wait_for_year_to)


@find_for_me_router.message(FindForMeStates.wait_for_year_to)
async def process_year_to(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1900 <= int(message.text) <= 2050):
        await message.answer(_('❌ Invalid year. Enter a number like 2020:'))
        return
    await state.update_data(year_to=int(message.text))
    await message.answer(_('💰 Budget from (USD):'))
    await state.set_state(FindForMeStates.wait_for_budget_from)


@find_for_me_router.message(FindForMeStates.wait_for_budget_from)
async def process_budget_from(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(_('❌ Budget must be a number. Try again:'))
        return
    await state.update_data(budget_from=message.text)
    await message.answer(_('💰 Budget to (USD):'))
    await state.set_state(FindForMeStates.wait_for_budget_to)


@find_for_me_router.message(FindForMeStates.wait_for_budget_to)
async def process_budget_to(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(_('❌ Budget must be a number. Try again:'))
        return

    await state.update_data(budget_to=message.text)
    await message.answer(_('📝 Want to tell us anything specific?\nDescribe it or press skip:'), reply_markup=skip_keyboard())
    await state.set_state(FindForMeStates.wait_for_specific_message)

@find_for_me_router.message(FindForMeStates.wait_for_specific_message)
async def process_specific_message(message: Message, state: FSMContext):
    await state.update_data(specific_message=message.text.strip())
    await ask_confirmation(message, state)