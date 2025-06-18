from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from auction_api.serializers import serialize_lot
from auction_api.utils import fetch_lot
from database.crud.user import UserService
from database.crud.user_search_history import UserSearchHistoryService
from database.schemas.user_search_history import UserSearchHistoryCreate
from telegram_bot.keyboards.inline.additional_lot_data import lot_inline_keyboard
from telegram_bot.utils.callback_query import parse_callback_data

choose_one_lot_router = Router()

@choose_one_lot_router.callback_query(F.data.startswith("open_lot_"))
async def open_lot(query: CallbackQuery):
    lot_id, auction = parse_callback_data(query.data)
    response = await fetch_lot(lot_id, auction)
    for lot in response:
        text = serialize_lot(lot)
        message = await query.message.answer(text, reply_markup=lot_inline_keyboard(lot_id, auction))
        images = lot.link_img_hd
        keyboard = lot_inline_keyboard(lot.lot_id, lot.base_site)

        if images:
            media = InputMediaPhoto(media=str(images[0]), caption=text)
            await message.edit_media(media=media, text=text, reply_markup=keyboard)

        async with UserService() as user_service:
            user = await user_service.get_by_telegram_id(query.from_user.id)
            async with UserSearchHistoryService() as user_search_history:
                await user_search_history.create(UserSearchHistoryCreate(
                    lot_id=lot.lot_id,
                    auction_name=lot.base_site,
                    user_id=user.id
                ))
    await query.answer()

