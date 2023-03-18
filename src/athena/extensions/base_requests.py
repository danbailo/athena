from enum import StrEnum

from typing import Any


from httpx import AsyncClient, Response

from pydantic import BaseModel


class MethodEnum(StrEnum):
    get = 'get'
    post = 'post'
    patch = 'patch'
    delete = 'delete'


# TODO: Apply tenancity
async def async_fetch(
    method: MethodEnum, url: str,
    data: dict[str, Any] | BaseModel | None = None,
    json: dict[str, Any] | BaseModel | None = None,
    params: dict[str, Any] | BaseModel | None = None,
    cookies: dict[str, Any] | None = None,
    headers: dict[str, Any] | BaseModel = {'Content-Type': 'application/json'},
    *args, **kwargs
) -> Response:
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
    async with AsyncClient() as client:
        response = await client.request(
            method, url, data=data, json=json, params=params,
            cookies=cookies, headers=headers, *args, **kwargs
        )
    return response
