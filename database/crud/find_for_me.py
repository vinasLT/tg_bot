from database.crud.base import BaseService
from database.models.find_for_me import FindForMe
from database.schemas.find_for_me import FindForMeCreate, FindForMeUpdate


class FindForMeService(BaseService[FindForMe, FindForMeCreate, FindForMeUpdate]):
    def __init__(self):
        super().__init__(FindForMe)

    async def __aenter__(self):
        await super().__aenter__()
        return self

