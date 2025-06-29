from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.crud.base import BaseService
from database.models.find_for_me import FindForMe
from database.schemas.find_for_me import FindForMeCreate, FindForMeUpdate


class FindForMeService(BaseService[FindForMe, FindForMeCreate, FindForMeUpdate]):
    def __init__(self):
        super().__init__(FindForMe)

    async def __aenter__(self):
        await super().__aenter__()
        return self

    async def is_user_have_unresponded_requests(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(FindForMe).where(
                FindForMe.user_id == user_id,
                FindForMe.is_responded.is_(False)
            )
        )
        return result.scalar() is not None

    async def get_all_active_requests(self) -> List[FindForMe]:
        result = await self.session.execute(
            select(FindForMe)
            .options(selectinload(FindForMe.user))
            .where(FindForMe.is_responded.is_(False))
        )
        return result.scalars().all()




