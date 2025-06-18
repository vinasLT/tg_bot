from pathlib import Path
from typing import Dict, Any

from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.i18n import I18nMiddleware, I18n

from database.crud.user import UserService

BASE_DIR = Path(__file__).resolve().parent.parent
i18n = I18n(path=BASE_DIR / "locales", default_locale="en", domain="messages")

class MyI18nMiddleware(I18nMiddleware):
    async def get_locale(
        self,
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> str:
        tg_user = None
        if isinstance(event, Message):
            tg_user = event.from_user
        elif isinstance(event, CallbackQuery):
            tg_user = event.from_user

        if not tg_user:
            return self.i18n.default_locale

        async with UserService() as db:
            db_user = await db.get_by_telegram_id(tg_user.id)

        if db_user and getattr(db_user, "language", None):
            return db_user.language

        if getattr(tg_user, "language_code", None):
            return tg_user.language_code

        return self.i18n.default_locale