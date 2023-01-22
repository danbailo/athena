from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from httpx import HTTPStatusError

from starlette.authentication import requires


from constants.mapped_api_prefix import MAPPED_API_ENDPOINT_PREFIX

from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from serializers.auth_serializer import TokenRequestHeaders

from .base_router import AlertTypeEnum, async_render_template, flash

from ..forms.user_form import LoginForm, RegisterForm

router = APIRouter(
    prefix=MAPPED_API_ENDPOINT_PREFIX['user']
)


@router.get('/admin')
@requires('admin')
async def user_admin_page(request: Request):
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
        await flash(request, 'Not authorized!', AlertTypeEnum.danger)
        return await async_render_template(
            'errors/403_error.html', request, 403,
        )

    return await async_render_template(
        'admin_template.html', request,
        context_request={'response': response}
    )


@router.get('')
@requires('authenticated', redirect='user_login_page')
async def user_page(request: Request):
    return await async_render_template('user_template.html', request, 200)


@router.get('/login', response_class=HTMLResponse | RedirectResponse)
async def user_login_page(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(router.url_path_for('user_page'), 302)
    return await async_render_template('login_template.html', request, 200)


@router.post('/login', response_class=RedirectResponse | HTMLResponse)
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
        await flash(request, 'User or password incorrect!', 'danger')
        return await async_render_template(
            'login_template.html', request, 401
        )
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404
        )
    response.set_cookie(
        key='access_token',
        value=f'{data["token_type"]} {data["access_token"]}',
        httponly=True
    )
    await flash(request, 'Successfully logged!', 'success')
    return RedirectResponse(
        router.url_path_for('user_page'), 302, response.headers
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


@router.get('/register', response_class=HTMLResponse)
async def user_register_page(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(router.url_path_for('user_page'), 302)
    return await async_render_template('register_template.html', request, 200)


@router.post('/register')
async def user_register(
    request: Request,
    response: Response,
    form_data: RegisterForm = Depends(RegisterForm.as_form)
):
    raise NotImplementedError()


@router.get('/features', response_class=HTMLResponse)
async def user_features_page(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(router.url_path_for('user_page'), 302)
    return await async_render_template('features_template.html', request, 200)


@router.post('/features')
async def user_features(
    request: Request
):
    raise NotImplementedError()
