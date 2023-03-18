from asyncpg.exceptions import UniqueViolationError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from sqlalchemy import insert, select, delete, update


from extensions.logger import logger

from serializers.section_serializer import (
    CreateSectionRequestBody, CreateSubSectionRequestBody,
    PatchSectionRequestBody
)
from serializers.user_serializer import UserResponseBody

from .auth_router import async_get_current_user


from ..database.connection import database
from ..database.models.section_model import SectionModel, SubSectionModel
from ..database.models.user_model import UserModel, RoleEnum

from ..utils.exceptions import (
    NotAuthorizedError, NothingToPatchError, NotPossibleDeleteAdmin,
    UserNotFoundError
)


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(
        self, user: UserModel = Depends(async_get_current_user)
    ):
        if user.role not in self.allowed_roles:
            logger.debug(
                f'User with role {user.role} not in {self.allowed_roles}'
            )
            raise NotAuthorizedError()


router = APIRouter()


@router.get(
    '/user',
    response_model=list[UserResponseBody],
    dependencies=[Depends(RoleChecker(['admin']))]
)
async def get_list_users(
    username: str | None = None,
    page: int = 0, limit: int = 30
):
    if username:
        query = select(UserModel).where(UserModel.username == username)
    else:
        query = select(UserModel)
    result = await database.fetch_all(query)
    return result[page: page+limit]


@router.get('/user/{id}', response_model=UserResponseBody)
async def get_user(id: int):
    query = select(UserModel).where(UserModel.id == id)
    if result := await database.fetch_one(query):
        return result
    raise UserNotFoundError()


@router.delete('/user/{id}', response_class=Response)
async def delete_user(id: int):
    query = select(UserModel).where(UserModel.id == id)
    if not (user := await database.fetch_one(query)):
        raise UserNotFoundError()
    if user.role == RoleEnum.admin:
        raise NotPossibleDeleteAdmin()
    query = delete(UserModel).where(UserModel.id == id)
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/section', status_code=204,
             dependencies=[Depends(RoleChecker('admin'))])
async def create_section(body: CreateSectionRequestBody):
    query = insert(SectionModel).values(**body.dict(by_alias=False))
    try:
        await database.execute(query)
    except UniqueViolationError:
        raise HTTPException(
            detail=f'The title `{body.title}` already is used!',
            status_code=400)


@router.patch('/section/{id}', status_code=204,
              dependencies=[Depends(RoleChecker('admin'))])
async def patch_section(id: int, body: PatchSectionRequestBody):
    if not (data := body.dict(exclude_none=True, by_alias=False)):
        raise NothingToPatchError()
    query = update(SectionModel).where(SectionModel.id == id).values(**data)
    try:
        await database.execute(query)
    except Exception as err:
        raise HTTPException(status_code=400, detail=err)


@router.post(
    '/section/{title_slug}/subsections',
    response_model=CreateSubSectionRequestBody,
    dependencies=[Depends(RoleChecker('admin'))])
async def create_subsection(
    title_slug: str, body: CreateSubSectionRequestBody
):
    query = select(SectionModel).where(SectionModel.title_slug == title_slug)
    if not (section := await database.fetch_one(query)):
        raise HTTPException(
            400, detail=f'Section `{title_slug}` does not exists!')
    values = body.dict()
    values.update({'section_id': section.id})
    query = insert(SubSectionModel)
    await database.execute(query, values=values)
    return body
