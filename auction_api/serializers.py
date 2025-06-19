from typing import Union

from auction_api.types import BasicLot, BasicHistoryLot
from aiogram.utils.i18n import gettext as _

def get_serialized_auction(base_site:str) -> str:
    return '🔴 IAAI' if base_site.lower() == 'iaai' else '🔵 COPART'

def serialize_lot(data: Union[BasicLot, BasicHistoryLot]) -> str:
    vehicle_name = f"{data.year if data.year else 'XXXX'} " \
                   f"{data.make.upper() if data.make else 'N/A'} " \
                   f"{data.model.upper() if data.model else 'N/A'} " \
                   f"{data.series.upper() if data.series else 'N/A'}"

    lines = [
        _("<b>☑️ {vehicle_name}</b>").format(vehicle_name=vehicle_name),
        _("<b>☑️ Lot ID:</b> <code>{lot_id}</code>").format(lot_id=data.lot_id),
        _("<b>☑️ VIN:</b> <code>{vin}</code>").format(vin=data.vin),
        _("<b>☑️ Auction:</b> {auction_name}").format(
            auction_name=get_serialized_auction(data.base_site)
        ),
        _("<b>☑️ Insurance:</b> {insurance}").format(
            insurance='Yes' if data.seller_type == 'insurance' else 'No'
        ),
        _("<b>☑️ Title:</b> {title}").format(title=data.document or 'N/A'),
        "",
        _("<b>🔥 Current bid:</b> <b>${current_bid}</b>").format(
            current_bid=data.current_bid if data.current_bid is not None else 'N/A'
        ),
    ]

    if data.is_buynow:
        lines.append(
            _("<b>🔥 BuyNow price:</b> <b>${buy_now}</b>").format(
                buy_now=data.price_new
            )
        )

    lines.extend([
        _("<b>🔥 Auction Status:</b> <b>{status}</b>").format(
            status=data.form_get_type.upper() if data.form_get_type else 'N/A'
        ),
        _("<b>🔥 Auction Date:</b> <i>{auction_date}</i>").format(
            auction_date=data.auction_date.strftime('%m/%d/%Y %H:%M') if data.auction_date is not None else 'N/A'
        ),
    ])

    return "\n".join(lines)

def serialize_preview_lot(data: Union[BasicLot, BasicHistoryLot]) -> str:
    vehicle_name = f"{data.year if data.year else 'XXXX'} " \
                   f"{data.make.upper() if data.make else 'N/A'} " \
                   f"{data.model.upper() if data.model else 'N/A'}"

    return "\n".join([
        _("<b>☑️ {vehicle_name}</b>").format(vehicle_name=vehicle_name),
        _("<b>☑️ Lot ID:</b> <code>{lot_id}</code>").format(lot_id=data.lot_id),
        _("<b>☑️ VIN:</b> <code>{vin}</code>").format(vin=data.vin),
        _("<b>☑️ Auction:</b> {auction_name}").format(
            auction_name=get_serialized_auction(data.base_site)
        ),
    ])

def serialize_history(data: BasicLot) -> str:
    history = data.sale_history
    text = ''
    if not history and not data.form_get_type == "history":

        return _('<b>❌ No history available</b>')
    for num, i in enumerate(history):
        text += _(
            "<b>🔹 History #{num}</b>\n"
            "☑️ <b>Lot ID:</b> <code>{lot_id}</code>\n"
            "☑️ <b>Auction:</b> {auction}\n"
            "☑️ <b>Date:</b> {date}\n"
            "☑️ <b>Price:</b> ${price}\n"
            "☑️ <b>Status:</b> <b>{status}</b>\n"
        ).format(
            num=num + 1,
            lot_id=i.lot_id,
            auction=get_serialized_auction(i.base_site),
            date=i.sale_date.strftime("%Y-%m-%d"),
            price=i.purchase_price if i.purchase_price is not None else 'N/A',
            status=i.sale_status.upper()
        )

        if num < len(history) - 1:
            text += "─────────────────\n"


    return text

def serialize_about_car(data: Union[BasicLot, BasicHistoryLot]) -> str:
    return _(
        "🛒 Seller Type: {seller_type}\n"
        "🚗 Cylinders: {cylinders}\n"
        "🔑 Keys: {keys}\n"
        "📏 Odometer: {odometer}\n"
        "⚙️ Engine: {engine} {engine_size}L\n"
        "⛽ Fuel: {fuel}\n"
        "🚙 Drive: {drive}\n"
        "🔧 Transmission: {transmission}\n"
        "🌍 Country: {country}"
    ).format(
        seller_type=data.seller_type.upper() if data.seller_type else 'N/A',
        cylinders=data.cylinders or 'N/A',
        keys=data.keys or 'N/A',
        odometer=f"{data.odometer:,}" if data.odometer is not None else 'N/A',
        engine=data.engine or 'N/A',
        engine_size=f"{data.engine_size:.1f}" if data.engine_size is not None else 'N/A',
        fuel=data.fuel or 'N/A',
        drive=data.drive or 'N/A',
        transmission=data.transmission or 'N/A',
        country=data.country.upper() if data.country else 'N/A',
    )