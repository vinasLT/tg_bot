from typing import Union

from external_apis.auction_api.types import BasicLot, BasicHistoryLot


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






