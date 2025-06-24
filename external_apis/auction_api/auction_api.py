import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Generic, List, Optional, Sequence, Type, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from external_apis.auction_api.types import (
    BasicLot,
    BasicHistoryLot,
    VINorLotIDIn,
    LotByVINIn,
    LotByIDIn,
    CurrentBidOut,
)
from config import API_SERVICE_URL
from external_apis.base import BaseAPIClient, Endpoint


class AuctionAPI(BaseAPIClient):
    _GET_LOT_BY_VIN_OR_ID: Endpoint[BasicLot] = Endpoint(
        path="/cars/",
        method="GET",
        request_model=VINorLotIDIn,
        response_model=BasicLot,
        response_model_history=BasicHistoryLot,
        is_list=True,
    )

    _GET_CURRENT_BID: Endpoint[CurrentBidOut] = Endpoint(
        path="/cars/current-bid/",
        method="GET",
        request_model=LotByIDIn,
        response_model=CurrentBidOut,
    )

    _GET_SALE_HISTORY_BY_VIN: Endpoint[BasicHistoryLot] = Endpoint(
        path="/cars/history/vin/",
        method="GET",
        request_model=LotByVINIn,
        response_model=BasicHistoryLot,
        is_list=True,
    )

    _GET_SALE_HISTORY_BY_ID: Endpoint[BasicHistoryLot] = Endpoint(
        path="/cars/history/lot-id/",
        method="GET",
        request_model=LotByIDIn,
        response_model=BasicHistoryLot,
        is_list=True,
    )

    async def get_lot_by_vin_or_id(self, params: VINorLotIDIn) -> List[BasicLot]:
        return await self.request(self._GET_LOT_BY_VIN_OR_ID, params)

    async def get_current_bid(self, params: LotByIDIn) -> CurrentBidOut:
        return await self.request(self._GET_CURRENT_BID, params)

    async def get_sale_history_by_vin(self, params: LotByVINIn) -> List[BasicHistoryLot]:
        return await self.request(self._GET_SALE_HISTORY_BY_VIN, params)

    async def get_sale_history_by_id(self, params: LotByIDIn) -> List[BasicHistoryLot]:
        return await self.request(self._GET_SALE_HISTORY_BY_ID, params)