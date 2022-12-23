from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from httpx import HTTPStatusError

from starlette.authentication import requires


from constants.mapped_prefix import MAPPED_API_ENDPOINT_PREFIX

from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from serializers.context_serializer import AlertTypeEnum

from .base_router import async_render_template

from ..forms.login_form import LoginForm


router = APIRouter(
    prefix=MAPPED_API_ENDPOINT_PREFIX['user']
)


@router.get('')
@requires('authenticated')
async def user_page(request: Request):
    return await async_render_template(
        'user_template.html', request, 200
    )


@router.get('/login', response_class=HTMLResponse)
async def user_login_page(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(
            request.base_url, 302,
            headers={'X-Athena-Authenticated': 'User already been logged!'}
        )
    return await async_render_template(
        'login_template.html', request, 200
    )


@router.post('/login', response_class=RedirectResponse)
async def user_login(
    request: Request,
    response: Response,
    form_data: LoginForm = Depends(LoginForm.as_form)
):
    url = get_env_var("ATHENA_API_BASE_URL", raise_exception=True)
    try:
        data = await async_fetch(
            MethodEnum.post,
            f'{url}/auth/token',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=form_data.dict(by_alias=True)
        )
    except HTTPStatusError:
        return await async_render_template(
            'login_template.html', request, 401,
            'Incorrect Username or Password', AlertTypeEnum.warning,
        )
    except Exception as exc:
        return await async_render_template(
            'errors/404_error.html', request, 404,
            'Unexpected error', AlertTypeEnum.danger, exc
        )
    response.set_cookie(
        key="access_token",
        value=f'{data["token_type"]} {data["access_token"]}',
        httponly=True
    )
    return RedirectResponse(
        request.base_url, 302, response.headers
    )


@router.get('/logout')
@requires('authenticated')
async def user_logout(request: Request):
    response = RedirectResponse(
        router.url_path_for('user_login'), 302
    )
    response.delete_cookie(key='access_token')
    return response
