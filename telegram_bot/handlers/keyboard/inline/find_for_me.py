from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from auction_api.auction_api import AuctionAPI
from auction_api.serializers import serialize_lot
from auction_api.types import VINorLotIDIn
from database.crud.find_for_me import FindForMeService
from database.crud.user import UserService
from database.schemas.find_for_me import FindForMeCreate, FindForMeUpdate
from telegram_bot.keyboards.inline.additional_lot_data import lot_inline_keyboard
from telegram_bot.keyboards.inline.find_for_me import new_find_for_me_request_received
from telegram_bot.states.find_for_me import FindForMeStates
from telegram_bot.utils.callback_query import parse_callback_data
from telegram_bot.utils.find_for_me import get_summary_text, ask_confirmation, send_lot

find_for_me_inline_router = Router()

#ADMIN
@find_for_me_inline_router.callback_query(F.data.startswith("respond_find_request_"))
async def respond_find_request_(query: CallbackQuery, state: FSMContext):
    data = query.data.split('_')
    request_id = data[-1]
    async with FindForMeService() as service:
        request = await service.get(int(request_id))
    if request.is_responded:
        await query.message.edit_text(_("✅ You already respond to this request!"), reply_markup=None)
        await query.answer()
        return
    await state.set_state(FindForMeStates.wait_for_lot_id)
    await state.update_data(request_id=request_id)
    await query.message.answer(_('🚘 Enter lot ID'))
    await query.answer()

@find_for_me_inline_router.callback_query(F.data.startswith("find_for_me_choose_auction_"))
async def find_for_me_choose_auction(query: CallbackQuery):
    lot_id, auction_name = parse_callback_data(query.data)
    loading_message = await query.message.answer(_('⏳ Loading...'))
    async with AuctionAPI() as api:
        response = await api.get_lot_by_vin_or_id(VINorLotIDIn(vin_or_lot=lot_id, site=auction_name))
        item = response[0]
        await send_lot(loading_message, item)

@find_for_me_inline_router.callback_query(F.data.startswith("confirm_respond_find_for_me_"))
async def confirm_respond_find_for_me(query: CallbackQuery, state: FSMContext):
    from main import bot
    lot_id, auction_name = parse_callback_data(query.data)
    data = await state.get_data()
    async with FindForMeService() as find_for_me_service:
        request = await find_for_me_service.get(int(data.get('request_id', 0)))
        if not request.is_responded:
            await find_for_me_service.update(
                request.id,
                FindForMeUpdate(is_responded=True, response_auction=auction_name, response_lot_id=int(lot_id))
            )
            user_id = request.user_id
            async with UserService() as user_service:
                user = await user_service.get(user_id)
                user_telegram_id = user.telegram_id

            async with AuctionAPI() as api:
                response = await api.get_lot_by_vin_or_id(VINorLotIDIn(vin_or_lot=lot_id, site=auction_name))
                item = response[0]
                images = item.link_img_hd
                text = serialize_lot(item)

                if images:
                    image_url = str(images[0])
                    await bot.send_message(
                        chat_id=user_telegram_id,
                        text=_('👋 <b>Hey, someone from our team answered your request, see what we have found for you!</b>')
                    )
                    await bot.send_photo(
                        chat_id=user_telegram_id,
                        photo=image_url,
                        caption=text,
                        reply_markup=lot_inline_keyboard(item.lot_id, item.base_site)
                    )

            await query.message.delete()

            await query.message.answer(_('✅ Successfully sent to user!'))
        else:
            await query.message.edit_text(_('✅ You already respond to this request!'), reply_markup=None)

        await query.answer()
        await state.clear()




#USER
@find_for_me_inline_router.callback_query(F.data == 'start_find_for_me')
async def start_find_for_me(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(_('🚘 Write the make:'), reply_markup=None)
    await state.set_state(FindForMeStates.wait_for_make)
    await query.answer()

@find_for_me_inline_router.callback_query(F.data == "confirm_find_for_me")
async def confirm_send(query: CallbackQuery, state: FSMContext):
    from main import bot
    data = await state.get_data()
    async with UserService() as user_service:
        user = await user_service.get_by_telegram_id(query.from_user.id)
        async with FindForMeService() as service:
            request = await service.create(FindForMeCreate(year_to=data.get('year_to'), make=data.get('make'), year_from=data.get('year_from'),
                                                 model=data.get('model'), budget_from=data.get('budget_from'), budget_to=data.get('budget_to'), specific_message=data.get('specific_message'), user_id=user.id))

        await query.message.edit_text(_('✅ Your request has been saved!'))
        await query.answer()

        text = get_summary_text(data)
        await state.clear()

        text += _("\n<b>NEW FIND FOR ME REQUEST RECIEVED!</b>")
        admins = await user_service.get_admins()

        for admin in admins:
            await bot.send_message(chat_id=admin.telegram_id, text=text,
                                   reply_markup=new_find_for_me_request_received(request.id))

@find_for_me_inline_router.callback_query(F.data == "skip_specific_message")
async def skip_specific_message(query: CallbackQuery, state: FSMContext):
    await state.update_data(specific_message=None)
    await ask_confirmation(query.message, state)
    await query.answer()


