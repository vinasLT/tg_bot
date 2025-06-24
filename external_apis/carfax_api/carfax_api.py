import asyncio
from typing import List

from config import CARFAX_SERVICE_URL
from external_apis.base import BaseAPIClient, Endpoint
from external_apis.carfax_api.types import Carfax, RequestCarfaxVin, ExternalUserIDSourceIn


class CarfaxAPI(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=CARFAX_SERVICE_URL)

    _BUY_CARFAX: Endpoint[Carfax] = Endpoint(
        path="/carfax/buy-carfax",
        method="POST",
        request_model=RequestCarfaxVin,
        response_model=Carfax,
    )

    _GET_CARFAX_LIST: Endpoint[Carfax] = Endpoint(
        path="/carfax",
        method="GET",
        request_model=ExternalUserIDSourceIn,
        response_model=Carfax,
        is_list=True,
    )

    _GET_CARFAX_BY_VIN: Endpoint[Carfax] = Endpoint(
        path="/carfax/{vin}/",
        method="GET",
        request_model=RequestCarfaxVin,
        response_model=Carfax,
    )


    async def buy_carfax(self, params: RequestCarfaxVin) -> Carfax:
        return await self.request(self._BUY_CARFAX, params)

    async def get_all_carfaxes(self, params: ExternalUserIDSourceIn) -> List[Carfax]:
        return await self.request(self._GET_CARFAX_LIST, params)

    async def get_carfax_by_vin(self, params: RequestCarfaxVin) -> Carfax:
        return await self.request(self._GET_CARFAX_BY_VIN, params)


if __name__ == '__main__':
    async def main():
        async with CarfaxAPI() as carfax:
            print(await carfax.get_carfax_by_vin(RequestCarfaxVin(user_external_id='23455656', source='telegram_bot', vin='KL4CJCSB6KB747856')))
    asyncio.run(main())




