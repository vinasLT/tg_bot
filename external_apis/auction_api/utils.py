from google._upb._message import RepeatedScalarContainer

from rpc_client.gen.python.auction.v1 import lot_pb2


def get_some_num_of_images(data: lot_pb2.Lot, num:int)-> list:
    if isinstance(data.link_img_hd, RepeatedScalarContainer):
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






