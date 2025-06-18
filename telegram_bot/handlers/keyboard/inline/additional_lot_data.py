from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from auction_api.auction_api import AuctionApiClient
from auction_api.serializers import serialize_about_car, serialize_history
from auction_api.types import EndpointSchema

from auction_api.utils import fetch_lot, get_some_num_of_images
from aiogram.utils.i18n import gettext as _

from telegram_bot.utils.callback_query import parse_callback_data

lot_additional_data_router = Router()



async def handle_lot_query(query: CallbackQuery, processor, endpoint: EndpointSchema = None):
    vin_or_id, auction_name = parse_callback_data(query.data)
    items = await fetch_lot(vin_or_id, auction_name, endpoint=endpoint)
    if items is None:
        await query.message.reply(_("❌ Something went wrong, try again later"))
        await query.answer()
        return
    await processor(query.message, items)
    await query.answer()

async def about_car_processor(message: Message, items):
    for item in items:
        await message.reply(serialize_about_car(item))

async def history_processor(message: Message, items):
    for item in items:
        await message.reply(serialize_history(item))


async def photos_processor(message: Message, items):
    for item in items:
        images = get_some_num_of_images(item, 11)[1:]
        if not images:
            await message.answer(_("🔍 No more images available."))
            continue
        media_group = [InputMediaPhoto(media=url) for url in images]
        await message.answer_media_group(media_group)

@lot_additional_data_router.callback_query(F.data.startswith("sales_statistics_"))
async def sales_statistics(query: CallbackQuery):
    await handle_lot_query(query, history_processor, AuctionApiClient.GET_SALE_HISTORY_BY_ID)

@lot_additional_data_router.callback_query(F.data.startswith("more_photos_"))
async def more_photos(query: CallbackQuery):
    await handle_lot_query(query, photos_processor)

@lot_additional_data_router.callback_query(F.data.startswith("about_car_"))
async def about_car(query: CallbackQuery):
    await handle_lot_query(query, about_car_processor)
