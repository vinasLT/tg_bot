from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.keyboards.inline.choose_auction import choose_auction
from telegram_bot.states.start_keyboard import StartKeyboardStates
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _


start_keyboard_handler = Router()


@start_keyboard_handler.message(F.text == __("Check lot 🚗"))
async def find_lot_handler(message: Message, state: FSMContext):
    await message.answer(_('Enter lot ID or VIN:'))
    await state.set_state(StartKeyboardStates.get_lot)

@start_keyboard_handler.message(StartKeyboardStates.get_lot)
async def start_lot_handler(message: Message, state: FSMContext):
    lot_id = message.text
    await message.answer(_('Choose auction:'), reply_markup=choose_auction(lot_id))
    await state.set_state(StartKeyboardStates.choose_auction)



