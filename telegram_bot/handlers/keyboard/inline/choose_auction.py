import time

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.i18n import gettext as _

from auction_api.auction_api import AuctionApiClient
from auction_api.types import VINorLotIDIn
from auction_api.utils import serialize_lot, get_first_3_images, get_api_client

choose_auction_router = Router()

@choose_auction_router.callback_query(F.data.startswith('choose_'))
async def choose_auction(query: CallbackQuery, state: FSMContext):
    data = query.data.split('_')
    auction = data[1]
    lot_id_or_vin = data[-1]
    api = get_api_client()

    start_total = time.monotonic()

    await query.message.answer(_('⏳ Loading...'))

    t_api = time.monotonic()
    response = await api.request_with_schema(
        AuctionApiClient.GET_LOT_BY_VIN_OR_ID,
        VINorLotIDIn(site=auction, vin_or_lot=lot_id_or_vin)
    )
    print(f"⏱ API запрос: {time.monotonic() - t_api:.2f} сек")

    t_loop = time.monotonic()
    if isinstance(response, list):
        for item in response:
            t_one = time.monotonic()

            images = get_first_3_images(item)
            text = serialize_lot(item)

            if images:
                media = [InputMediaPhoto(media=url) for url in images[:10]]
                media[0].caption = text
                await query.message.answer_media_group(media)
            else:
                await query.message.answer(text)

            print(f"⏱ Один лот отправлен за: {time.monotonic() - t_one:.2f} сек")
    print(f"⏱ Обработка всех лотов: {time.monotonic() - t_loop:.2f} сек")

    await query.answer()
    await state.clear()

    print(f"✅ Общая обработка: {time.monotonic() - start_total:.2f} сек")
