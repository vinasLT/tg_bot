def parse_callback_data(data: str) -> tuple[str, str]:
    *_, vin_or_id, auction_name = data.split("_")
    return vin_or_id, auction_name