from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from ..routers.base_router import AlertTypeEnum, async_render_template, flash


async def async_403_http_error_exception_handler(
    request: Request, exc: HTTPException
):
    await flash(request, 'Not authorized!', AlertTypeEnum.danger)
    return RedirectResponse('/', 302)


async def async_404_http_error_exception_handler(
    request: Request, exc: HTTPException
):
    await flash(request, str(exc), AlertTypeEnum.danger)
    return await async_render_template(
        'errors/404_error.html', request, exc.status_code,
    )
