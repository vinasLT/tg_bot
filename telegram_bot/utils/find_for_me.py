from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from external_apis.auction_api import serialize_lot
from external_apis.auction_api import BasicLot
from telegram_bot.keyboards.inline.find_for_me import confirm_keyboard
from telegram_bot.states.find_for_me import FindForMeStates
from aiogram.utils.i18n import gettext as _

def get_summary_text(data: dict)->str:
    summary = _(
        "<b>🚘 Make:</b> {make}\n"
        "<b>📦 Model:</b> {model}\n"
        "<b>📅 Year From:</b> {year_from}\n"
        "<b>📅 Year To:</b> {year_to}\n"
        "<b>💰 Budget From:</b> {budget_from}$\n"
        "<b>💰 Budget To:</b> {budget_to}$\n"
    ).format(year_to=data.get('year_to'), make=data.get('make'), year_from=data.get('year_from'),
             model=data.get('model'), budget_from=data.get('budget_from'), budget_to=data.get('budget_to'))

    if data.get("specific_message"):
        summary += _("<b>📝 Note:</b> {specific_message}\n").format(specific_message=data["specific_message"])

    return summary

async def ask_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()

    summary = get_summary_text(data)

    summary += _("\n✅ Do you want to send this request?")

    await message.answer(summary, reply_markup=confirm_keyboard())
    await state.set_state(FindForMeStates.wait_for_confirmation)

async def send_lot(editable_message: Message, item: BasicLot):
    images = item.link_img_hd
    text = serialize_lot(item)

    if images:
        media = InputMediaPhoto(media=str(images[0]), caption=text)
        await editable_message.edit_media(media=media, text=text, reply_markup=confirm_keyboard(
            f'confirm_respond_find_for_me_{item.lot_id}_{item.base_site}'))