from fastapi import APIRouter

from sqlalchemy import select, func, and_


from serializers.section_serializer import (
    SectionResponseBody, SubSectionResponseBody, CountSectionResponseBody
)

from .base_router import CommonQuery

from database.connection import database
from database.models.section_model import SectionModel, SubSectionModel
from database.models.base import select_database

from utils.exceptions import ItemNotFoundError

router = APIRouter()


async def async_get_subsections_from_section(
    section_id: int
) -> list[SubSectionResponseBody]:
    query = select(SubSectionModel).where(
        SubSectionModel.section_id == section_id)
    return await database.fetch_all(query)


@router.get('/{section_id}/subsection/count',
            response_model=CountSectionResponseBody)
async def count_subsections_from_section(section_id: int):
    query = select(func.count()).select_from(SubSectionModel).where(
        SubSectionModel.section_id == section_id)
    return {'count': await database.execute(query)}


@router.get('/{section_id}/subsection/{subsection_id}',
            response_model=SubSectionResponseBody)
async def get_subsection(section_id: int, subsection_id: int):
    query = select(SubSectionModel).where(and_(
        SectionModel.id == section_id,
        SubSectionModel.id == subsection_id
    ))
    if result := await database.fetch_one(query):
        return result
    raise ItemNotFoundError()


@router.get(
    '/{section_id}/subsection',
    response_model=list[SubSectionResponseBody])
async def get_subsections_from_section(
    section_id: int,
    is_visible: bool | None = None,
    common: CommonQuery = None,
):
    query = select(SectionModel).where(SectionModel.id == section_id)
    if not (section := await database.fetch_one(query)):
        raise ItemNotFoundError()
    query = select_database(
        SubSectionModel, [
            {'section_id': section.id, 'sub_visible': is_visible}
        ], page=common.page, limit=common.limit)
    return await database.fetch_all(query)


@router.get('/subsection', response_model=list[SubSectionResponseBody])
async def get_list_subsections(
    title: str | None = None,
    title_slug: str | None = None,
    sub_visible: bool | None = None,
    common: CommonQuery = None,
):
    query = select_database(
        SubSectionModel, [
            {'title': title, 'title_slug': title_slug, 'visible': sub_visible},
        ], common.page, common.limit, order_by=[
            SubSectionModel.sub_order_to_show.asc(), SubSectionModel.id.asc()])
    return await database.fetch_all(query)


@router.get('', response_model=list[SectionResponseBody])
async def get_list_sections(
    title: str | None = None,
    title_slug: str | None = None,
    is_visible: bool | None = None,
    common: CommonQuery = None,
):
    query = select_database(SectionModel, [
        {'title': title, 'title_slug': title_slug, 'visible': is_visible},
    ], common.page, common.limit, order_by=[
        SectionModel.order_to_show.asc(), SectionModel.id.asc()])
    to_return = [SectionResponseBody(**section)
                 for section in await database.fetch_all(query)]
    for section in to_return:
        section.subsections = await async_get_subsections_from_section(
            section.id)
    return to_return


@router.get('/count', response_model=CountSectionResponseBody)
async def count_sections():
    query = select(func.count()).select_from(SectionModel)
    return {'count': await database.execute(query)}


@router.get('/{section_id}', response_model=SectionResponseBody)
async def get_section(section_id: int):
    query = select(SectionModel).where(SectionModel.id == section_id)
    if result := await database.fetch_one(query):
        to_return = SectionResponseBody(**result)
        to_return.subsections = await async_get_subsections_from_section(
            to_return.id)
        return to_return
    raise ItemNotFoundError()
