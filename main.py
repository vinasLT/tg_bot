import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_BOT_TOKEN
from telegram_bot.handlers.commands.start import start
from telegram_bot.handlers.keyboard.inline.additional_lot_data import lot_additional_data_router
from telegram_bot.handlers.keyboard.inline.cancel import cancel_router
from telegram_bot.handlers.keyboard.inline.choose_language import choose_language_router
from telegram_bot.handlers.keyboard.inline.choose_one_lot import choose_one_lot_router
from telegram_bot.handlers.keyboard.murkup.main_keyboard import start_keyboard_handler
from telegram_bot.middelwares import MyI18nMiddleware, i18n

bot = Bot(token=API_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    MyI18nMiddleware(i18n).setup(dp)

    dp.include_router(start)
    dp.include_router(cancel_router)
    dp.include_router(start_keyboard_handler)
    dp.include_router(lot_additional_data_router)
    dp.include_router(choose_one_lot_router)
    dp.include_router(choose_language_router)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    print('project starts')
    asyncio.run(main())