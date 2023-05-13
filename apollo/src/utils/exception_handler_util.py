from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from pydantic import ValidationError


from routers.base_router import AlertTypeEnum, async_render_template, flash

MAPPED_URL_TEMPLATE = {
    '/user/register': 'register_template.html',
    '/user/login': 'login_template.html'
}


async def async_403_http_error_exception_handler(
    request: Request, exc: HTTPException
):
    return RedirectResponse('/', 302)


async def async_404_http_error_exception_handler(
    request: Request, exc: HTTPException
):
    await flash(request, str(exc), AlertTypeEnum.danger)
    return await async_render_template(
        'errors/404_error.html', request, exc.status_code,
    )


async def async_validation_error_exception_handler(
    request: Request, exc: ValidationError
):
    for error in exc.errors():
        await flash(request, error['msg'], AlertTypeEnum.danger)
    return await async_render_template(
        MAPPED_URL_TEMPLATE[request.url.path], request, 400,
        {'form': exc.model.get_form_values()}
    )
