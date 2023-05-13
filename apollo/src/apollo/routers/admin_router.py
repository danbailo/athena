from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse

from httpx import HTTPStatusError

from starlette.authentication import requires


from extensions.env_var import get_env_var
from extensions.base_requests import async_fetch, MethodEnum

from serializers.auth_serializer import TokenRequestHeaders

from .base_router import AlertTypeEnum, flash, async_render_template

from ..forms.section_form import CreateSectionForm, UpdateSectionForm


router = APIRouter(prefix='/admin')


@router.get('')
@requires('admin')
async def admin_home_page(request: Request):
    return await async_render_template(
        'admin/admin_index_template.html', request
    )


@router.get('/user')
@requires('admin')
async def admin_user_page(request: Request):
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    data = {}
    try:
        response = await async_fetch(
            MethodEnum.get,
            f'{base_url}/admin/user',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
        response.raise_for_status()
        data = response.json()
    except HTTPStatusError:
        await flash(request, data.get('detail'), AlertTypeEnum.danger)
        return await async_render_template(
            'errors/403_error.html', request, 403,
        )
    return await async_render_template(
        'admin/admin_user_template.html', request,
        context_request={'data': data}
    )


@router.get('/user/{id}')
@requires('admin')
async def admin_user_detail_page(request: Request, id: int):
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    data = {}
    try:
        response = await async_fetch(
            MethodEnum.get,
            f'{base_url}/admin/user/{id}',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
        response.raise_for_status()
        data = response.json()
    except HTTPStatusError:
        await flash(request, data.get('detail'), AlertTypeEnum.danger)
        return await async_render_template(
            'errors/403_error.html', request, 403,
        )
    return await async_render_template(
        'admin/admin_user_detail_template.html', request,
        context_request={'data': data}
    )


@router.post('/user/delete/{id}')
@requires('admin')
async def admin_delete_user(request: Request, id: int):
    data = {}
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.delete,
            f'{base_url}/admin/user/{id}',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
        response.raise_for_status()
    except HTTPStatusError:
        if response.content.decode():
            data = response.json()
        await flash(request, data.get('detail') or '', AlertTypeEnum.danger)
        return RedirectResponse(request.url_for('admin_user_page'),
                                status_code=302)
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404,
        )
    return RedirectResponse(request.url_for('admin_user_page'),
                            status_code=302)


@router.get('/section')
@requires('admin')
async def admin_section_page(request: Request, page: int = 1, limit: int = 5):
    data = {}
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.get,
            f'{base_url}/section',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            ),
            params={'page': page, 'limit': limit}
        )
        response.raise_for_status()
        data = response.json()

        response = await async_fetch(
            MethodEnum.get, f'{base_url}/section/count')
        count = response.json()
    except HTTPStatusError:
        await flash(request, data.get('detail'), AlertTypeEnum.danger)
        return await async_render_template(
            'errors/403_error.html', request, 403,
        )
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404,
        )
    return await async_render_template(
        'admin/admin_section_template.html', request,
        context_request={
            'data': data,
            'create_section_form': CreateSectionForm.get_form_values(),
            'count': count,
            'limit': limit}
    )


@router.post('/section/create', response_class=HTMLResponse | RedirectResponse)
@requires('admin')
async def admin_create_section(
    request: Request,
    form_data: CreateSectionForm = Depends(CreateSectionForm.as_form)
):
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    try:
        _response = await async_fetch(
            MethodEnum.post, f'{base_url}/admin/section',
            json=form_data,
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
        _response.raise_for_status()
    except HTTPStatusError:
        await flash(request, _response.json()['detail'], 'danger')
        return RedirectResponse(
            request.url_for('admin_section_page'), status_code=302)
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404
        )
    return RedirectResponse(
        request.url_for('admin_section_page'), status_code=302)


@router.get('/section/{id}')
@requires('admin')
async def admin_section_detail_page(request: Request, id: int):
    data = {}
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.get,
            f'{base_url}/section/{id}',
            headers=TokenRequestHeaders(
                access_token=request.headers['cookie']
            )
        )
        response.raise_for_status()
        data = response.json()
    except HTTPStatusError:
        await flash(request, data.get('detail') or '', AlertTypeEnum.danger)
        return await async_render_template(
            'errors/403_error.html', request, 403,
        )
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404,
        )
    return await async_render_template(
        'admin/admin_section_detail_template.html', request,
        context_request={'data': data}
    )


@router.post('/section/patch/{id}')
@requires('admin')
async def admin_patch_section(
    request: Request,
    id: int,
    form_data: UpdateSectionForm = Depends(UpdateSectionForm.as_form)
):
    data = {}
    base_url = get_env_var('ATHENA_ARES_BASE_URL')
    try:
        response = await async_fetch(
            MethodEnum.patch,
            f'{base_url}/admin/section/{id}',
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
        return RedirectResponse(
            request.url_for('admin_section_detail_page', id=id),
            status_code=302)
    except Exception as exc:
        await flash(request, f'Unexpected error! - {str(exc)}', 'danger')
        return await async_render_template(
            'errors/404_error.html', request, 404,
        )
    return RedirectResponse(
        request.url_for('admin_section_detail_page', id=id), status_code=302)
