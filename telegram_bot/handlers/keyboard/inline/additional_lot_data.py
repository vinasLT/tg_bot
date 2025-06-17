from typing import Union, List, Type

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from httpx import HTTPStatusError

from auction_api.auction_api import AuctionApiClient
from auction_api.types import LotByVINIn, VINorLotIDIn
from auction_api.utils import get_api_client, serialize_history, get_some_num_of_images
from aiogram.utils.i18n import gettext as _


lot_additional_data_router = Router()

@lot_additional_data_router.callback_query(F.data.startswith('sales_statistics_'))
async def sales_statistics(query: CallbackQuery):
    data = query.data.split('_')
    auction_name = data[-1]
    vin = data[-2]
    api = get_api_client()
    try:
        response = await api.request_with_schema(AuctionApiClient.GET_SALE_HISTORY_BY_VIN, LotByVINIn(vin=vin, site=auction_name))
        print(response)
    except HTTPStatusError:
        await query.message.reply(_('❌ Something went wrong, try again later'))
        await query.answer()
        return

    if isinstance(response, list):
        for item in response:
            if item.form_get_type == 'history':
                print('history')
                text = serialize_history(item)
                await query.message.reply(text)
                await query.answer()
    else:
        if response.form_get_type == 'history':
            text = serialize_history(response)
            await query.message.reply(text)
            await query.answer()

@lot_additional_data_router.callback_query(F.data.startswith('more_photos_'))
async def more_photos(query: CallbackQuery):
    data = query.data.split('_')
    auction_name = data[-1]
    lot_id = data[-2]
    api = get_api_client()

    try:
        response = await api.request_with_schema(
            AuctionApiClient.GET_LOT_BY_VIN_OR_ID,
            VINorLotIDIn(vin_or_lot=lot_id, site=auction_name)
        )
    except HTTPStatusError:
        await query.message.reply(_('❌ Something went wrong, try again later'))
        await query.answer()
        return

    items = response if isinstance(response, list) else [response]

    for item in items:
        images = get_some_num_of_images(item, 11)[1:]
        if not images:
            await query.message.answer(_('🔍 No more images available.'))
            continue

        media_group = [InputMediaPhoto(media=url) for url in images]
        await query.message.answer_media_group(media=media_group)

    await query.answer()






