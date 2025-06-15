import logging
from typing import Optional

from sqlalchemy import select

from database.crud.base import BaseService
from database.models.user import User
from database.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)



class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    async def __aenter__(self):
        await super().__aenter__()
        return self

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()
