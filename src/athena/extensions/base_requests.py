from enum import StrEnum

from typing import Any


from httpx import AsyncClient


class MethodEnum(StrEnum):
    get = 'get'
    post = 'post'
    patch = 'patch'
    delete = 'delete'


# TODO: Apply tenancity
async def async_fetch(
    method: MethodEnum, url: str, data: dict[str, Any] | Any,
    headers={'Content-Type': 'application/json'}
):
    async with AsyncClient() as client:
        response = await client.request(
            method, url, data=data,
            headers=headers
        )
        response.raise_for_status()
    return response.json()
