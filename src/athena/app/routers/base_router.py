from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates


from serializers.context_serializer import AlertTypeEnum, ContextSerializer

templates = Jinja2Templates(directory="app/templates")


async def async_render_template(
    template_name: str, context_request: Request, status_code: int,
    alert_msg: str = '', alert_type: AlertTypeEnum | None = None,
    exc: HTTPException | None = None, headers: dict[str, str] | None = None
):
    if exc:
        alert_msg += getattr(exc, 'detail', None) or str(exc)
    return templates.TemplateResponse(
        template_name,
        ContextSerializer(
            request=context_request,
            msg=alert_msg,
            alert_type=alert_type
        ).dict(),
        status_code=status_code,
        headers=headers
    )


async def handle_403_http_error(request: Request, exc: HTTPException):
    response = RedirectResponse('/user/login', 302)
    response.headers['X-Unauthenticated'] = 'User must be authenticated!'
    return response


async def handle_404_http_error(request: Request, exc: HTTPException):
    return await async_render_template(
        'errors/404_error.html', request, exc.status_code,
        alert_type=AlertTypeEnum.danger, exc=exc
    )
