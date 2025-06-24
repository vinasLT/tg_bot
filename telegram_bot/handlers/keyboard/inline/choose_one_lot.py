import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from external_apis.auction_api import AuctionAPI
from external_apis.auction_api import serialize_lot
from external_apis.auction_api import LotByIDIn, VINorLotIDIn
from database.crud.user_search_history import UserSearchHistoryService
from telegram_bot.handlers.errors.get_lot import get_lot_errors
from telegram_bot.keyboards.inline.additional_lot_data import lot_inline_keyboard
from telegram_bot.utils.callback_query import parse_callback_data


choose_one_lot_router = Router()

choose_one_lot_router.error.register(get_lot_errors)


@choose_one_lot_router.callback_query(F.data.startswith("open_lot_"))
async def open_lot(query: CallbackQuery):
    lot_id, auction = parse_callback_data(query.data)

    async with AuctionAPI() as api:
        lots = await api.get_lot_by_vin_or_id(
            VINorLotIDIn(vin_or_lot=lot_id, site=auction)
        )

        messages: list[Message] = []
        for lot in lots:
            text = serialize_lot(lot)
            msg = await query.message.answer(
                text,
                reply_markup=lot_inline_keyboard(lot.lot_id, lot.base_site),
            )
            messages.append(msg)

            if lot.link_img_hd:
                await msg.edit_media(
                    media=InputMediaPhoto(media=str(lot.link_img_hd[0]), caption=text),
                    reply_markup=lot_inline_keyboard(lot.lot_id, lot.base_site),
                )

            async with UserSearchHistoryService() as svc:
                await svc.save_user_search(query.from_user.id, lot.lot_id, auction)

        await query.answer()

        active_pairs = [
            (lot, msg)
            for lot, msg in zip(lots, messages)
            if lot.form_get_type.lower() == "active"
        ]
        if active_pairs:
            bids = await asyncio.gather(
                *(
                    api.get_current_bid(
                        LotByIDIn(lot_id=lot.lot_id, site=auction)
                    )
                    for lot, _ in active_pairs
                )
            )
            for (lot, msg), bid in zip(active_pairs, bids):
                lot.current_bid = bid.pre_bid
                await msg.edit_text(serialize_lot(lot))





