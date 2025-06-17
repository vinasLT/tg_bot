from database.crud.base import BaseService
from database.models.user_search_history import UserSearchHistory
from database.schemas.user_search_history import UserSearchHistoryCreate, UserSearchHistoryUpdate


class UserSearchHistoryService(BaseService[UserSearchHistory, UserSearchHistoryCreate, UserSearchHistoryUpdate]):
    def __init__(self):
        super().__init__(UserSearchHistory)

    async def __aenter__(self):
        await super().__aenter__()
        return self