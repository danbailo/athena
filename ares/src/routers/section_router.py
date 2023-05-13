from fastapi import APIRouter

from sqlalchemy import select, func


from serializers.section_serializer import (
    SectionResponseBody, SubSectionResponseBody, CountSectionResponseBody
)

from .base_router import CommonQuery

from database.connection import database
from database.models.section_model import SectionModel, SubSectionModel
from database.models.base import select_database


from utils.exceptions import ItemNotFoundError

router = APIRouter()


@router.get('/count', response_model=CountSectionResponseBody)
async def count_sections():
    query = select(func.count()).select_from(SectionModel)
    return {'count': await database.execute(query)}


@router.get('/{id}', response_model=SectionResponseBody)
async def get_section(id: int):
    query = select(SectionModel).where(SectionModel.id == id)
    if result := await database.fetch_one(query):
        return result
    raise ItemNotFoundError()


@router.get('', response_model=list[SectionResponseBody])
async def get_list_sections(
    title: str | None = None,
    title_slug: str | None = None,
    common: CommonQuery = None,
):
    query = select_database(SectionModel, [
        {'title': title, 'title_slug': title_slug}
    ], common.page, common.limit)
    return await database.fetch_all(query)


@router.get(
    '/{title_slug}/subsection',
    response_model=list[SubSectionResponseBody])
async def get_list_subsections(
    title_slug: str,
    common: CommonQuery = None,
):
    query = select(SectionModel).where(SectionModel.title_slug == title_slug)
    if not (section := await database.fetch_one(query)):
        raise ItemNotFoundError()
    query = select_database(SubSectionModel, [{'section_id': section.id}],
                            page=common.page, limit=common.limit)
    return await database.fetch_all(query)
