from database.crud.base import BaseService
from database.crud.user import UserService
from database.models.user_search_history import UserSearchHistory
from database.schemas.user_search_history import UserSearchHistoryCreate, UserSearchHistoryUpdate


class UserSearchHistoryService(BaseService[UserSearchHistory, UserSearchHistoryCreate, UserSearchHistoryUpdate]):
    def __init__(self):
        super().__init__(UserSearchHistory)

    async def __aenter__(self):
        await super().__aenter__()
        return self

    async def save_user_search(self, user_id: int, lot_id: int, auction: str):
        async with UserService() as user_service:
            user = await user_service.get_by_telegram_id(user_id)
            await self.create(UserSearchHistoryCreate(
                lot_id=lot_id,
                auction_name=auction,
                user_id=user.id
            ))