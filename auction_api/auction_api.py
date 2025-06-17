from abc import abstractmethod
from typing import List, Type

from pydantic import BaseModel

import httpx

from auction_api.types import EndpointSchema, BasicLot, BasicHistoryLot, VINorLotIDIn, LotByVINIn
from config import API_SERVICE_URL


class AuctionAPIBase:
    SERVER_URL = API_SERVICE_URL
    def __init__(self):
        self.session = httpx.AsyncClient(timeout=10.0)

    def _build_url(self, url: str) -> str:
        return f"{self.SERVER_URL.rstrip('/')}/{url.lstrip('/')}"

    async def _make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        return await self.session.request(method, url, **kwargs)

    async def request_with_schema(self, schema: EndpointSchema, data: BaseModel) -> Type[BaseModel] | Type[List[BaseModel]]:
        payload = data.model_dump(exclude_none=True)
        url = self._build_url(schema.endpoint)

        if schema.method == "GET":
            response = await self._make_request("GET", url, params=payload)
        elif schema.method == "POST":
            response = await self._make_request("POST", url, json=payload)
        else:
            raise ValueError(f"Unsupported method: {schema.method}")
        print(response)
        response.raise_for_status()

        response_data = response.json()
        print(response_data)

        return self.process_response(response_data, schema)

    @abstractmethod
    def process_response(self, response_data: dict | list, schema: EndpointSchema) -> Type[BaseModel] | Type[List[BaseModel]]:
        ...


class AuctionApiClient(AuctionAPIBase):
    GET_LOT_BY_VIN_OR_ID = EndpointSchema(
        validation_schema=VINorLotIDIn,
        endpoint='cars/',
        method='GET',
        out_schema_default=BasicLot,
        out_schema_history=BasicHistoryLot,
        is_list=True,
    )
    GET_SALE_HISTORY_BY_VIN = EndpointSchema(
        validation_schema=LotByVINIn,
        endpoint='cars/history/vin',
        method='GET',
        out_schema_default=BasicHistoryLot,
    )

    def __init__(self):
        super().__init__()

    @staticmethod
    def is_item_history(item: dict) -> bool:
        if item.get('form_get_type') == 'active':
            return False
        elif item.get('form_get_type') == 'history':
            return True
        else:
            return False

    def process_response(self, response_data: dict | list, schema: EndpointSchema):
        if not schema.out_schema_history is None:
            if schema.is_list:
                items = response_data if isinstance(response_data, list) else [response_data]
                return [
                    (schema.out_schema_history if self.is_item_history(
                        item) else schema.out_schema_default).model_validate(
                        item)
                    for item in items
                ]

            out_schema = schema.out_schema_history if self.is_item_history(response_data) else schema.out_schema_default
        else:
            out_schema = schema.out_schema_default

        return out_schema.model_validate(response_data)


