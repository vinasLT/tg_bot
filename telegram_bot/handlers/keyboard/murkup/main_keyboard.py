from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from external_apis.auction_api.auction_api import AuctionAPI
from external_apis.auction_api.serializers import serialize_lot, serialize_preview_lot
from external_apis.auction_api.types import VINorLotIDIn
from database.crud.user import UserService
from database.crud.user_search_history import UserSearchHistoryService
from telegram_bot.handlers.errors.get_lot import get_lot_errors
from telegram_bot.keyboards.inline.additional_lot_data import lot_inline_keyboard
from telegram_bot.keyboards.inline.calculator_link import calculator_link
from telegram_bot.keyboards.inline.cancel import cancel_keyboard
from telegram_bot.keyboards.inline.carfax import carfax
from telegram_bot.keyboards.inline.choose_language import choose_language
from telegram_bot.keyboards.inline.choose_one_lot import choose_one_lot
from telegram_bot.states.start_keyboard import StartKeyboardStates
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

start_keyboard_handler = Router()

start_keyboard_handler.error.register(get_lot_errors)

@start_keyboard_handler.message(F.text == __("CHECK LOT 🕵‍♂"))
async def find_lot_handler(message: Message, state: FSMContext):
    await message.answer(_('🚘 Enter lot ID or VIN:'), reply_markup=cancel_keyboard())
    await state.set_state(StartKeyboardStates.wait_for_vin_or_lot)



@start_keyboard_handler.message(F.text == __('LANGUAGE 🌍'))
async def process_language(message: Message):
    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(message.from_user.id)
        await message.answer(_('🌎 Choose language'), reply_markup=choose_language(user.language))


@start_keyboard_handler.message(F.text == __('TRANSPORT COST CALC. 💸'))
async def transport_calculator(message: Message):
    await message.answer(_('💸 Click on the button below to open the calculator'), reply_markup=calculator_link())

@start_keyboard_handler.message(F.text == __('HELP ✋'))
async def transport_calculator(message: Message):
    await message.answer(_('<b>ℹ Help:</b>\n'
                           '✉ My email: <b>hvjlogistic@gmail.com</b>\n'
                           '📞 My WhatsApp/Viber/Telegram/Signal: <b>+37062964425</b>\n'
                           ))

@start_keyboard_handler.message(F.text == __('GET REPORT 🦊'))
async def get_carfax(message: Message, state: FSMContext):
    await message.answer(_('You can buy a detailed report about the car (🦊 Carfax)'), reply_markup=carfax())


@start_keyboard_handler.message(StartKeyboardStates.wait_for_vin_or_lot)
@start_keyboard_handler.message(StartKeyboardStates.wait_for_vin_or_lot)
async def process_vin_or_lot_id(message: Message, state: FSMContext):
    vin_or_lot_id = message.text

    loading_message = await message.answer(_('⏳ Loading...'))

    async with AuctionAPI() as api:
        response = await api.get_lot_by_vin_or_id(VINorLotIDIn(vin_or_lot=vin_or_lot_id))

    await state.clear()

    if len(response) >= 2:
        # Если пришло два лота
        two_lots = _('<b>We received 2 lots according to your data, choose below what you need</b>\n\n')
        for num, item in enumerate(response):
            two_lots += f'<b>#{num + 1}</b>\n'
            two_lots += serialize_preview_lot(item)
            two_lots += '\n\n'

        await loading_message.edit_text(two_lots, reply_markup=choose_one_lot(response))
        return

    # Если пришёл только один лот
    item = response[0]
    images = item.link_img_hd
    text = serialize_lot(item)
    keyboard = lot_inline_keyboard(item.lot_id, item.base_site)

    # Сохраняем в историю
    async with UserSearchHistoryService() as user_history_service:
        await user_history_service.save_user_search(message.from_user.id, item.lot_id, item.base_site)

    if images:
        # Удаляем сообщение "⏳ Loading..." и отправляем фото с подписью и клавиатурой
        await loading_message.delete()
        await message.answer_photo(
            photo=str(images[0]),
            caption=text,
            reply_markup=keyboard,
        )
    else:
        # Если изображений нет, редактируем сообщение и добавляем клавиатуру
        await loading_message.edit_text(text, reply_markup=keyboard)




