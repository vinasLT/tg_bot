from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from external_apis.auction_api.serializers import serialize_about_car, serialize_history

from external_apis.auction_api.utils import get_some_num_of_images
from aiogram.utils.i18n import gettext as _

from rpc_client.api_client import ApiRpcClient
from telegram_bot.utils.callback_query import parse_callback_data

lot_additional_data_router = Router()


@lot_additional_data_router.callback_query(F.data.startswith("sales_statistics_"))
async def sales_statistics(query: CallbackQuery):
    vin_or_id, auction_name = parse_callback_data(query.data)
    print('data_recvieved')
    async with ApiRpcClient() as rpc_client:
        print('request start')
        response = await rpc_client.get_sale_history(lot_id=int(vin_or_id), site=auction_name)
        print('request end')
        lots = response.lot
        for item in lots:
            await query.message.reply(serialize_history(item))

    await query.answer()

@lot_additional_data_router.callback_query(F.data.startswith("more_photos_"))
async def more_photos(query: CallbackQuery):
    vin_or_id, auction_name = parse_callback_data(query.data)

    async with ApiRpcClient() as rpc_client:
        response = await rpc_client.get_lot_by_vin_or_lot_id(vin_or_lot_id=vin_or_id, site=auction_name)
        lots = response.lot

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
    async with ApiRpcClient() as rpc_client:
        lots = await rpc_client.get_lot_by_vin_or_lot_id(vin_or_lot_id=vin_or_id, site=auction_name)

    for item in lots.lot:
        await query.message.reply(serialize_about_car(item))
    await query.answer()
