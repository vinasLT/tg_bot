import asyncio
import logging
import re
from dataclasses import dataclass
from typing import Type, Optional, Generic, Any, Sequence, List, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from config import API_SERVICE_URL

R = TypeVar("R", bound=BaseModel)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclass(slots=True)
class Endpoint(Generic[R]):
    path: str
    method: str
    request_model: Type[BaseModel]
    response_model: Type[R]
    response_model_history: Optional[Type[BaseModel]] = None
    is_list: bool = False

class BaseAPIClient:
    def __init__(
        self,
        base_url: str = API_SERVICE_URL,
        *,
        timeout: float = 10.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
        self._client: httpx.AsyncClient | None = client

    async def __aenter__(self) -> "BaseAPIClient":
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                headers = {"Accept": "application/json"},
                follow_redirects = True
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._client:
            await self._client.aclose()

    async def _send(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> httpx.Response:
        assert self._client is not None
        attempt = 0
        while True:
            try:
                response = await self._client.request(method, path, params=params, json=json)
                logger.info('headers: %s', response.request.headers)
                print('headers: ', response.request.headers)
                response.raise_for_status()
                return response
            except (httpx.TransportError, httpx.HTTPStatusError) as exc:
                if exc.response is not None and exc.response.status_code in (404, 500):
                    raise
                attempt += 1
                if attempt > self._max_retries:
                    logger.error("%s %s failed after %s attempts: %s", method, path, attempt, exc)
                    raise
                sleep_for = self._backoff_factor * 2 ** (attempt - 1)
                logger.warning("Request error (%s). Retrying in %.1fs…", exc, sleep_for)
                await asyncio.sleep(sleep_for)

    @staticmethod
    def _is_history(item: dict[str, Any]) -> bool:
        return item.get("form_get_type") == "history"

    @staticmethod
    def _format_path(path: str, data: dict[str, Any]) -> str:
        def replace(match: re.Match) -> str:
            key = match.group(1)
            if key not in data:
                raise ValueError(f"Missing path parameter: {key}")
            return str(data.pop(key))
        return re.sub(r"{(\w+)}", replace, path)

    async def request(self, endpoint: Endpoint[R], payload: BaseModel) -> List[R] | R:
        data = payload.model_dump(exclude_none=True)

        path = self._format_path(endpoint.path, data)

        if endpoint.method.upper() == "GET":
            response = await self._send("GET", path, params=data)
        elif endpoint.method.upper() == "POST":
            response = await self._send("POST", path, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {endpoint.method}")

        raw = response.json()

        if endpoint.is_list:
            raw_items: Sequence[dict[str, Any]] = raw if isinstance(raw, list) else [raw]
            validated: List[R] = []
            for item in raw_items:
                model_cls: Type[BaseModel] = (
                    endpoint.response_model_history
                    if endpoint.response_model_history and self._is_history(item)
                    else endpoint.response_model
                )
                try:
                    validated.append(model_cls.model_validate(item))
                except ValidationError as err:
                    logger.error("Validation failed for %s %s: %s", endpoint.method, endpoint.path, err)
                    raise
            return validated

        model_cls: Type[BaseModel] = (
            endpoint.response_model_history
            if endpoint.response_model_history and self._is_history(raw)
            else endpoint.response_model
        )
        try:
            return model_cls.model_validate(raw)
        except ValidationError as err:
            logger.error("Validation failed for %s %s: %s", endpoint.method, endpoint.path, err)
            raise