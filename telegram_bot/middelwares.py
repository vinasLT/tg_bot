from pathlib import Path
from typing import Dict, Any

from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.i18n import I18nMiddleware, I18n

from database.crud.user import UserService

BASE_DIR = Path(__file__).resolve().parent.parent
i18n = I18n(path=BASE_DIR / "locales", default_locale="en", domain="messages")

class MyI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return self.i18n.default_locale  # fallback если откуда-то ещё

        async with UserService() as db:
            user = await db.get_by_telegram_id(user_id)
            return user.language or self.i18n.default_locale