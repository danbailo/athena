from enum import StrEnum

import logging

from typing import Any


from tenacity import retry, stop_after_attempt, wait_fixed, before_log

from httpx import AsyncClient, Response, request


from pydantic import BaseModel

from extensions.logger import logger


class MethodEnum(StrEnum):
    get = 'get'
    post = 'post'
    patch = 'patch'
    delete = 'delete'


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    before=before_log(logger, logging.DEBUG),
)
async def async_fetch(
    method: MethodEnum, url: str,
    data: dict[str, Any] | BaseModel | None = None,
    json: dict[str, Any] | BaseModel | None = None,
    params: dict[str, Any] | BaseModel | None = None,
    cookies: dict[str, Any] | None = None,
    headers: dict[str, Any] | BaseModel = None,
    raise_for_status: bool = False,
    *args, **kwargs
) -> Response:
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    if isinstance(data, BaseModel):
        data = data.dict(by_alias=True)
    if isinstance(json, BaseModel):
        json = json.dict(by_alias=True)
    if isinstance(params, BaseModel):
        params = params.dict(by_alias=True)
    if isinstance(cookies, BaseModel):
        cookies = cookies.dict(by_alias=True)
    if isinstance(headers, BaseModel):
        headers = headers.dict(by_alias=True)
    async with AsyncClient(timeout=180) as client:
        response = await client.request(
            method, url, data=data, json=json, params=params,
            cookies=cookies, headers=headers, *args, **kwargs
        )
    if raise_for_status is True:
        response.raise_for_status()
    return response


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    before=before_log(logger, logging.DEBUG),
)
def _fetch(
    method: MethodEnum, url: str,
    data: dict[str, Any] | BaseModel | None = None,
    json: dict[str, Any] | BaseModel | None = None,
    params: dict[str, Any] | BaseModel | None = None,
    cookies: dict[str, Any] | None = None,
    headers: dict[str, Any] | BaseModel = None,
    raise_for_status: bool = False,
    *args, **kwargs
) -> Response:
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    if isinstance(data, BaseModel):
        data = data.dict(by_alias=True)
    if isinstance(json, BaseModel):
        json = json.dict(by_alias=True)
    if isinstance(params, BaseModel):
        params = params.dict(by_alias=True)
    if isinstance(cookies, BaseModel):
        cookies = cookies.dict(by_alias=True)
    if isinstance(headers, BaseModel):
        headers = headers.dict(by_alias=True)
    response = request(
        method, url, data=data, json=json, params=params,
        cookies=cookies, headers=headers, *args, **kwargs, timeout=180
    )
    if raise_for_status is True:
        response.raise_for_status()
    return response
