import httpx
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent
from pydantic_core import ValidationError
from aiogram.utils.i18n import gettext as _

async def get_lot_errors(event: ErrorEvent) -> bool:
    exc = event.exception
    if isinstance(exc, (ValidationError, httpx.TransportError, httpx.HTTPStatusError, TelegramBadRequest)):
        message = getattr(event.update, "message", None)
        print(message)
        if message:
            await message.answer(_("❌ We cant find your lot, try again"))
        return True

    return False