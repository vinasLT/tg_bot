from functools import lru_cache
from typing import Union

from httpx import HTTPStatusError

from auction_api.auction_api import AuctionApiClient
from auction_api.types import BasicLot, BasicHistoryLot, VINorLotIDIn, EndpointSchema, LotByIDIn


def get_some_num_of_images(data: Union[BasicLot, BasicHistoryLot], num:int)-> list:
    if isinstance(data.link_img_hd, list):
        images = []
        for image in data.link_img_hd[:num]:
            images.append(str(image))
        return images
    return []

def generate_link_to_auction(lot_id: int, auction_name: str) -> str:
    if auction_name.lower() == 'copart':
        return f'https://www.copart.com/lot/{lot_id}'
    else:
        return f'https://www.iaai.com/Search?Keyword={lot_id}'

async def fetch_lot(vin_or_id, site, endpoint: EndpointSchema = AuctionApiClient.GET_LOT_BY_VIN_OR_ID):
    api = get_api_client()
    data = LotByIDIn(lot_id=vin_or_id, site=site) if endpoint == AuctionApiClient.GET_SALE_HISTORY_BY_ID else VINorLotIDIn(vin_or_lot=vin_or_id, site=site)
    try:
        res = await api.request_with_schema(
            endpoint,
            data,
        )
        print(res)
        return res if isinstance(res, list) else [res]
    except HTTPStatusError:
        return None




@lru_cache
def get_api_client()-> AuctionApiClient:
    return AuctionApiClient()


