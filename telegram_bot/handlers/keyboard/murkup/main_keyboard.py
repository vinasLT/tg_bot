from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto
from httpx import HTTPStatusError

from auction_api.auction_api import AuctionApiClient
from auction_api.serializers import serialize_lot, serialize_preview_lot
from auction_api.types import VINorLotIDIn
from auction_api.utils import get_api_client
from database.crud.user import UserService
from database.crud.user_search_history import UserSearchHistoryService
from database.schemas.user_search_history import UserSearchHistoryCreate
from telegram_bot.keyboards.inline.additional_lot_data import lot_inline_keyboard
from telegram_bot.keyboards.inline.cancel import cancel_keyboard
from telegram_bot.keyboards.inline.choose_language import choose_language
from telegram_bot.keyboards.inline.choose_one_lot import choose_one_lot
from telegram_bot.states.start_keyboard import StartKeyboardStates
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _


start_keyboard_handler = Router()


@start_keyboard_handler.message(F.text == __("CHECK LOT 🕵‍♂"))
async def find_lot_handler(message: Message, state: FSMContext):
    await message.answer(_('🚘 Enter lot ID or VIN:'), reply_markup=cancel_keyboard())
    await state.set_state(StartKeyboardStates.wait_for_vin_or_lot)

@start_keyboard_handler.message(StartKeyboardStates.wait_for_vin_or_lot)
async def process_vin_or_lot_id(message: Message, state: FSMContext):
    vin_or_lot_id = message.text
    api = get_api_client()

    loading_message = await message.answer(_('⏳ Loading...'))
    async def edit_for_error_message(editable_message: Message):
        await editable_message.edit_text(_('❌ We cant find your lot, try again'), reply_markup=cancel_keyboard())

    try:
        response = await api.request_with_schema(AuctionApiClient.GET_LOT_BY_VIN_OR_ID, VINorLotIDIn(vin_or_lot=vin_or_lot_id))
    except HTTPStatusError:
        await edit_for_error_message(loading_message)
        return

    if len(response) >= 2:
        two_lots = _('<b>We received 2 lots according to your data, choose below what you need</b>\n\n')
        for num, item in enumerate(response):
            two_lots += f'<b>#{num + 1}</b>\n'
            two_lots += serialize_preview_lot(item)
            two_lots += '\n\n'

        await loading_message.edit_text(two_lots, reply_markup=choose_one_lot(response))
        await state.clear()
        return
    else:
        item = response[0]
        images = item.link_img_hd
        text = serialize_lot(item)

        async with UserService() as user_service:
            user = await user_service.get_by_telegram_id(message.from_user.id)
            async with UserSearchHistoryService() as user_search_history:
                await user_search_history.create(UserSearchHistoryCreate(
                    lot_id=item.lot_id,
                    auction_name=item.base_site,
                    user_id=user.id
                ))
        keyboard = lot_inline_keyboard(item.lot_id, item.base_site)

        if images:
            media = InputMediaPhoto(media=str(images[0]), caption=text)
            await loading_message.edit_media(media=media, text=text, reply_markup=keyboard)
        await state.clear()

@start_keyboard_handler.message(F.text == __('LANGUAGE 🌍'))
async def process_language(message: Message):
    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(message.from_user.id)
        await message.answer(_('🌎 Choose language'), reply_markup=choose_language(user.language))







