from asyncpg.exceptions import UniqueViolationError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from sqlalchemy import insert, select, delete, update, and_


from extensions.logger import logger

from serializers.section_serializer import (
    CreateSectionRequestBody, CreateSubSectionRequestBody,
    PatchSectionRequestBody, PatchSubSectionRequestBody
)
from serializers.user_serializer import UserResponseBody

from .auth_router import CurrentUser

from database.connection import database
from database.models.section_model import SectionModel, SubSectionModel
from database.models.user_model import UserModel, RoleEnum

from utils.exceptions import (
    NotAuthorizedError, NothingToPatchError, NotPossibleDeleteAdmin,
    UserNotFoundError, ItemNotFoundError
)


class RoleChecker:
    def __init__(self, allowed_roles: str | list[str]):
        if isinstance(allowed_roles, str):
            allowed_roles = [allowed_roles]
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUser):
        if user.role not in self.allowed_roles:
            logger.debug(
                'User with role %s not in %s', user.role, self.allowed_roles)
            raise NotAuthorizedError()


router = APIRouter()

CheckAdmin = Depends(RoleChecker(['admin']))


@router.get(
    '/user',
    response_model=list[UserResponseBody],
    dependencies=[CheckAdmin]
)
async def get_list_users(username: str | None = None):
    if username:
        query = select(UserModel).where(UserModel.username == username)
    else:
        query = select(UserModel)
    result = await database.fetch_all(query)
    return result


@router.get('/user/{user_id}', response_model=UserResponseBody)
async def get_user(user_id: int):
    query = select(UserModel).where(UserModel.id == user_id)
    if result := await database.fetch_one(query):
        return result
    raise UserNotFoundError()


@router.delete('/user/{user_id}', response_class=Response)
async def delete_user(user_id: int):
    query = select(UserModel).where(UserModel.id == user_id)
    if not (user := await database.fetch_one(query)):
        raise UserNotFoundError()
    if user.role == RoleEnum.admin:
        raise NotPossibleDeleteAdmin()
    query = delete(UserModel).where(UserModel.id == user_id)
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/section', status_code=204, dependencies=[CheckAdmin])
async def create_section(body: CreateSectionRequestBody):
    query = insert(SectionModel).values(**body.dict(by_alias=False))
    try:
        await database.execute(query)
    except UniqueViolationError as exc:
        raise HTTPException(
            detail=f'The title `{body.title}` already is used!',
            status_code=400) from exc


@router.patch('/section/{section_id}', status_code=204,
              dependencies=[CheckAdmin])
async def patch_section(section_id: int, body: PatchSectionRequestBody):
    if not (data := body.dict(exclude_none=True, by_alias=False)):
        raise NothingToPatchError()
    query = update(SectionModel).where(
        SectionModel.id == section_id).values(**data)
    try:
        await database.execute(query)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=exc) from exc


@router.delete('/section/{section_id}', status_code=204,
               dependencies=[CheckAdmin])
async def delete_section(section_id: int):
    query = select(SectionModel).where(SectionModel.id == section_id)
    if not await database.fetch_one(query):
        raise ItemNotFoundError()
    query = delete(SectionModel).where(SectionModel.id == section_id)
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/section/{section_id}/subsection',
    response_model=CreateSubSectionRequestBody,
    dependencies=[CheckAdmin])
async def create_subsection(
    section_id: int, body: CreateSubSectionRequestBody
):
    query = select(SectionModel).where(
        SectionModel.id == section_id)
    if not (section := await database.fetch_one(query)):
        raise HTTPException(
            400, detail=f'Section `{section_id}` does not exists!')
    values = body.dict(by_alias=False)
    values.update({'section_id': section.id})
    query = insert(SubSectionModel).values(**values)
    await database.execute(query)
    return body


@router.patch(
    '/section/{section_id}/subsection/{subsection_id}',
    dependencies=[CheckAdmin],
    status_code=204)
async def patch_subsection(
    section_id: int,
    subsection_id: int,
    body: PatchSubSectionRequestBody,
):
    if not (data := body.dict(exclude_none=True, by_alias=False)):
        raise NothingToPatchError()
    query = update(SubSectionModel).where(and_(
        SectionModel.id == section_id,
        SubSectionModel.id == subsection_id)).values(**data)
    try:
        await database.execute(query)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=exc) from exc


@router.delete(
    '/section/{section_id}/subsection/{subsection_id}',
    dependencies=[CheckAdmin],
    status_code=204)
async def delete_subsection(section_id: int, subsection_id: int):
    query = select(SubSectionModel).where(and_(
        SectionModel.id == section_id,
        SubSectionModel.id == subsection_id))
    if not await database.fetch_one(query):
        raise HTTPException(
            400, detail=f'Subsection `{subsection_id}` does not exists!')
    query = delete(SubSectionModel).where(and_(
        SectionModel.id == section_id,
        SubSectionModel.id == subsection_id))
    await database.execute(query)
