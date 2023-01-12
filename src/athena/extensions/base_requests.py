from enum import StrEnum

from typing import Any


from httpx import AsyncClient

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
    cookies: dict[str, Any] | None = None,
    headers={'Content-Type': 'application/json'}
):
    if isinstance(data, BaseModel):
        data = data.dict(by_alias=True)
    if isinstance(json, BaseModel):
        json = json.dict(by_alias=True)
    async with AsyncClient() as client:
        response = await client.request(
            method, url, data=data,
            json=json, cookies=cookies,
            headers=headers
        )
        response.raise_for_status()
    return response.json()
