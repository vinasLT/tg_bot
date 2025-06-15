import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_BOT_TOKEN
from telegram_bot.handlers.commands.start import start
from telegram_bot.handlers.keyboard.inline.cancel import cancel_router
from telegram_bot.handlers.keyboard.inline.choose_auction import choose_auction_router
from telegram_bot.handlers.keyboard.murkup.start import start_keyboard_handler
from telegram_bot.middelwares import MyI18nMiddleware, i18n

bot = Bot(token=API_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    MyI18nMiddleware(i18n).setup(dp)

    dp.include_router(start)
    dp.include_router(cancel_router)
    dp.include_router(choose_auction_router)
    dp.include_router(start_keyboard_handler)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    print('project starts')
    asyncio.run(main())