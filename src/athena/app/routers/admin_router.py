from fastapi import APIRouter, Request

from httpx import HTTPStatusError

from starlette.authentication import requires


from constants.mapped_api_prefix import MAPPED_API_ENDPOINT_PREFIX

from extensions.env_var import get_env_var
from extensions.base_requests import async_fetch, MethodEnum

from serializers.auth_serializer import TokenRequestHeaders

from .base_router import AlertTypeEnum, flash, async_render_template


router = APIRouter()


@router.get('/admin')
@requires('admin')
async def user_admin_page(request: Request):
    base_url = get_env_var('ATHENA_API_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.get,
            f'{base_url}{MAPPED_API_ENDPOINT_PREFIX["admin"]}',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
        response.raise_for_status()
        data = response.json()
    except HTTPStatusError:
        await flash(request, data['detail'], AlertTypeEnum.danger)
        return await async_render_template(
            'errors/403_error.html', request, 403,
        )

    return await async_render_template(
        'admin_template.html', request,
        context_request={'data': data}
    )
