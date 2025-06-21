from aiogram import Router, F
from aiogram.types import Message


from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from telegram_bot.keyboards.inline.find_for_me import find_for_me_start_cancel

find_for_me_router = Router()

@find_for_me_router.message(F.text == __('FIND FOR ME 🕵‍♂'))
async def find_for_me(message: Message):
    await message.answer(_('🔍 <b>How "Find for Me" works:</b>\n'
                           '<b>1.</b> You fill out a short form with:\n'
                           '– <b>Make</b>\n'
                           '– <b>Model</b>\n'
                           '– <b>Year</b>\n'
                           '– <b>Budget</b>\n'
                           '<b>2.</b> Our team searches for matching vehicles.\n'
                           '<b>3.</b> If you like the suggestion, <b>we help you buy and ship it!</b>'),
                         reply_markup=find_for_me_start_cancel())
