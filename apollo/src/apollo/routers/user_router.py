from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from httpx import HTTPStatusError

from starlette.authentication import requires


from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from .base_router import async_render_template, flash, AlertTypeEnum

from ..forms.user_form import LoginForm, RegisterForm, UpdateUserForm

from serializers.auth_serializer import TokenRequestHeaders

router = APIRouter(
    prefix='/user'
)


@router.get('/login', response_class=HTMLResponse | RedirectResponse)
async def user_login_page(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(router.url_path_for('user_page'), 302)
    return await async_render_template(
        'login_template.html', request, 200,
        {'form': LoginForm.get_form_values()}
    )


@router.get('', response_class=HTMLResponse)
@requires('authenticated', redirect='user_login_page')
async def user_page(request: Request):
    return await async_render_template(
        'user_template.html', request, 200, context_request={
            'user': request.user
        }
    )


@router.post('/login', response_class=RedirectResponse | HTMLResponse)
async def user_login(
    request: Request,
    response: Response,
    form_data: LoginForm = Depends(LoginForm.as_form)
):
    base_url = get_env_var('ATHENA_API_BASE_URL', raise_exception=True)
    data = {}
    try:
        _response = await async_fetch(
            MethodEnum.post,
            f'{base_url}/auth/token',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=form_data
        )
        data = _response.json()
        _response.raise_for_status()
    except HTTPStatusError:
        await flash(request, data.get('detail'), 'danger')
        return await async_render_template(
            'login_template.html', request, 401,
            {'form': form_data.get_form_values()}
        )
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404,
            {'form': form_data.get_form_values()}
        )
    response.set_cookie(
        key='access_token',
        value=f'{data["token_type"]} {data["access_token"]}',
        httponly=True
    )
    return RedirectResponse(
        router.url_path_for('user_page'), 302, response.headers
    )


@router.get('/logout', response_class=RedirectResponse)
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


@router.get('/register', response_class=HTMLResponse | RedirectResponse)
async def user_register_page(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(router.url_path_for('user_page'), 302)
    return await async_render_template(
        'register_template.html', request, 200,
        {'form': RegisterForm.get_form_values()}
    )


@router.post('/register', response_class=HTMLResponse | RedirectResponse)
async def user_register(
    request: Request,
    form_data: RegisterForm = Depends(RegisterForm.as_form)
):
    base_url = get_env_var('ATHENA_API_BASE_URL')
    try:
        _response = await async_fetch(
            MethodEnum.post, f'{base_url}/user',
            json=form_data
        )
        _response.raise_for_status()
    except HTTPStatusError:
        await flash(request, _response.json()['detail'], 'danger')
        return await async_render_template(
            'register_template.html', request, 401,
            {'form': form_data.get_form_values()}
        )
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404
        )
    await flash(request, 'Usuário registrado com sucesso!', 'success')
    return RedirectResponse(request.url_for('user_login'), status_code=302)


@router.post('/patch')
@requires('authenticated', redirect='user_page')
async def user_patch(
    request: Request,
    form_data: UpdateUserForm = Depends(UpdateUserForm.as_form)
):
    data = {}
    base_url = get_env_var('ATHENA_API_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.patch,
            f'{base_url}/user',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            ),
            json=form_data
        )
        response.raise_for_status()
    except HTTPStatusError:
        if response.content.decode():
            data = response.json()
        await flash(request, data.get('detail') or '', AlertTypeEnum.danger)
        return RedirectResponse(request.url_for('user_page'),
                                status_code=302)
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404,
        )
    return RedirectResponse(
        request.url_for('user_page'), status_code=302)


@router.get('/features', response_class=HTMLResponse | RedirectResponse)
async def user_features_page(request: Request):
    raise NotImplementedError()


@router.post('/features')
async def user_features(
    request: Request
):
    raise NotImplementedError()
