from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from serializers.context_serializer import AlertTypeEnum

from ..routers.base_router import async_render_template


async def async_403_http_error_exception_handler(
    request: Request, exc: HTTPException
):
    return RedirectResponse(
        '/user/login', 302,
        headers={'X-Athena-Flash-Message-Unauthenticated':
                 'User must be authenticated!'}
    )


async def async_404_http_error_exception_handler(
    request: Request, exc: HTTPException
):
    return await async_render_template(
        'errors/404_error.html', request, exc.status_code,
        alert_type=AlertTypeEnum.danger, exc=exc
    )
