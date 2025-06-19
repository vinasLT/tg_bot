from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from auction_api.auction_api import AuctionAPI
from auction_api.serializers import serialize_about_car, serialize_history
from auction_api.types import LotByIDIn, VINorLotIDIn

from auction_api.utils import get_some_num_of_images
from aiogram.utils.i18n import gettext as _

from telegram_bot.utils.callback_query import parse_callback_data

lot_additional_data_router = Router()


@lot_additional_data_router.callback_query(F.data.startswith("sales_statistics_"))
async def sales_statistics(query: CallbackQuery):
    vin_or_id, auction_name = parse_callback_data(query.data)
    async with AuctionAPI() as api:
        items = await api.get_sale_history_by_id(LotByIDIn(lot_id=vin_or_id, site=auction_name))
        for item in items:
            await query.message.reply(serialize_history(item))
    await query.answer()

@lot_additional_data_router.callback_query(F.data.startswith("more_photos_"))
async def more_photos(query: CallbackQuery):
    vin_or_id, auction_name = parse_callback_data(query.data)
    async with AuctionAPI() as api:
        lots = await api.get_lot_by_vin_or_id(
            VINorLotIDIn(vin_or_lot=vin_or_id, site=auction_name)
        )
        for item in lots:
            images = get_some_num_of_images(item, 11)[1:]
            if not images:
                await query.message.answer(_("🔍 No more images available."))
                continue
            media_group = [InputMediaPhoto(media=url) for url in images]
            await query.message.answer_media_group(media_group)
    await query.answer()

@lot_additional_data_router.callback_query(F.data.startswith("about_car_"))
async def about_car(query: CallbackQuery):
    vin_or_id, auction_name = parse_callback_data(query.data)
    async with AuctionAPI() as api:
        lots = await api.get_lot_by_vin_or_id(
            VINorLotIDIn(vin_or_lot=vin_or_id, site=auction_name)
        )
    for item in lots:
        await query.message.reply(serialize_about_car(item))
    await query.answer()
