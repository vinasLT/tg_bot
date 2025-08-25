from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from rpc_client.gen.python.carfax.v1 import carfax_pb2
from telegram_bot.keyboards.inline.cancel import cancel_button


def carfax()-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=_('🦊 See my CarFaxes'), callback_data=f'see_all_carfaxes'),
                    InlineKeyboardButton(text=_('💳 Buy CarFax (2€)'), callback_data=f'buy_new_carfax')
                ]
            ]
)

def buy_or_see(carfax_obj: carfax_pb2.Carfax)-> InlineKeyboardMarkup:
    if carfax_obj.is_paid:
        button = InlineKeyboardButton(text=_('🔗 Open CarFax'), url=str(carfax_obj.link))
    else:
        button = InlineKeyboardButton(text=_('💳 Buy'), callback_data=f'carfax_buy_{carfax_obj.vin}')

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button],
        ]
    )

def buy_or_cancel(vin: str)-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_('💳 Buy'), callback_data=f'carfax_buy_{vin}'),
             cancel_button()],
        ]
    )

def payment_link(link: str, vin: str)-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_('💳 Pay (2€)'), url=str(link)),
             InlineKeyboardButton(text=_('☑️ Check'), callback_data=f'check_payment_{vin}')],
        ]
    )