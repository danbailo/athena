from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response, RedirectResponse

from httpx import HTTPStatusError

from starlette.authentication import requires


from constants.mapped_api_prefix import MAPPED_API_ENDPOINT_PREFIX

from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from serializers.auth_serializer import TokenRequestHeaders
from serializers.context_serializer import AlertTypeEnum

from .base_router import async_render_template

from ..forms.login_form import LoginForm

router = APIRouter(
    prefix=MAPPED_API_ENDPOINT_PREFIX['user']
)


@router.get('/login', response_class=RedirectResponse)
async def user_login_page(request: Request):
    response = RedirectResponse(request.base_url, 304)
    if request.user.is_authenticated:
        response.headers['X-Athena-Flash-Message-Authenticated'] =\
            'User already been logged!'
    return response


@router.post('/login', response_class=RedirectResponse)
async def user_login(
    request: Request,
    response: Response,
    form_data: LoginForm = Depends(LoginForm.as_form)
):
    base_url = get_env_var('ATHENA_API_BASE_URL', raise_exception=True)
    try:
        data = await async_fetch(
            MethodEnum.post,
            f'{base_url}{MAPPED_API_ENDPOINT_PREFIX["auth"]}/token',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=form_data
        )
    except HTTPStatusError:
        response.headers['X-Athena-Flash-Message-Authenticated'] =\
            'Incorrect Username or Password'
        return RedirectResponse(
            request.base_url, 304, response.headers
        )
    except Exception as exc:
        return await async_render_template(
            'errors/404_error.html', request, 404,
            'Unexpected error', AlertTypeEnum.danger, exc
        )
    response.set_cookie(
        key='access_token',
        value=f'{data["token_type"]} {data["access_token"]}',
        httponly=True
    )
    return RedirectResponse(
        request.base_url, 302, response.headers
    )


@router.get('/logout')
async def user_logout(request: Request):
    if not request.user.is_authenticated:
        return RedirectResponse(
            request.base_url, 302,
            headers={'X-Athena-Flash-Message-Not-Authenticated':
                     'User must be authenticated!'}
        )
    response = RedirectResponse(
        request.base_url, 302
    )
    response.delete_cookie(key='access_token')
    return response


@router.get('/admin')
@requires('admin')
async def user_admin(request: Request):
    base_url = get_env_var('ATHENA_API_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.get,
            f'{base_url}{MAPPED_API_ENDPOINT_PREFIX["admin"]}/admin',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
    except HTTPStatusError:
        return await async_render_template(
            'errors/403_error.html', request, 403,
            'Not authorized!', AlertTypeEnum.danger
        )

    return await async_render_template(
        'admin_template.html', request,
        context_request={'response': response}
    )
