import asyncio

from pydantic import HttpUrl

from config import PAYMENT_SERVICE_URL
from external_apis.base import BaseAPIClient, Endpoint
from external_apis.payment_api.types import StripeCheckOutOut, StripeCheckOutIn


class PaymentAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=PAYMENT_SERVICE_URL)

    _GET_STRIPE_CHECKOUT: Endpoint[StripeCheckOutOut] = Endpoint(
        path="/stripe/get-checkout",
        method="POST",
        request_model=StripeCheckOutIn,
        response_model=StripeCheckOutOut,
    )

    async def get_stripe_checkout(self, params: StripeCheckOutIn) -> StripeCheckOutOut:
        return await self.request(self._GET_STRIPE_CHECKOUT, params)


if __name__ == '__main__':
    async def main():
        async with PaymentAPI() as api:
            response = await api.get_stripe_checkout(StripeCheckOutIn(external_user_id='324534590', purpose='CARFAX',
                                                                      purpose_external_id=1,
                                                                      success_link='https://google.com/',
                                                                      cancel_link='https://google.com/'))
    asyncio.run(main())
