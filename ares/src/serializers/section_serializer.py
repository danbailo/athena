from datetime import datetime


from pydantic import BaseModel, root_validator, Field, validator

from slugify import slugify


class CountSectionResponseBody(BaseModel):
    count: int


class CreateSectionRequestBody(BaseModel):
    title: str
    body: str
    visible: bool = False
    order_to_show: int = 0

    @root_validator
    @classmethod
    def set_title_slug(cls, root: dict[str, str]):
        if not root.get('title'):
            return root
        root['title_slug'] = slugify(root['title'])
        return root


class PatchSectionRequestBody(BaseModel):
    title: str | None = None
    body: str | None = None
    visible: bool | None = None
    order_to_show: int | None = None

    @root_validator
    @classmethod
    def set_title_slug(cls, root: dict[str, str]):
        if not root.get('title'):
            return root
        root['title_slug'] = slugify(root['title'])
        return root

    @root_validator
    @classmethod
    def set_last_updated(cls, root: dict[str, str]):
        if any(root.values()):
            root['last_updated'] = datetime.utcnow()
        return root


class CreateSubSectionRequestBody(BaseModel):
    sub_title: str = Field(..., alias='sub_title')
    sub_body: str = Field(..., alias='sub_body')
    sub_link_image: str | None = Field(None, alias='sub_link_image')
    sub_visible: bool = False
    sub_order_to_show: int = 0

    @root_validator
    @classmethod
    def set_sub_title_slug(cls, root: dict[str, str]):
        if not root.get('sub_title'):
            return root
        root['sub_title_slug'] = slugify(root['sub_title'])
        return root

    class Config:
        allow_population_by_field_name = True


class PatchSubSectionRequestBody(BaseModel):
    sub_title: str | None = Field(None, alias='sub_section_title')
    sub_body: str | None = Field(None, alias='sub_section_body')
    sub_link_image: str | None = Field(None, alias='sub_section_link_image')
    sub_visible: bool | None = None
    sub_order_to_show: int | None = None

    @root_validator
    @classmethod
    def set_title_slug(cls, root: dict[str, str]):
        if not root.get('sub_title'):
            return root
        root['sub_title_slug'] = slugify(root['sub_title'])
        return root

    @root_validator
    @classmethod
    def set_last_updated(cls, root: dict[str, str]):
        if any(root.values()):
            root['sub_last_updated'] = datetime.utcnow()
        return root

    class Config:
        allow_population_by_field_name = True


class SubSectionResponseBody(CreateSubSectionRequestBody):
    section_id: int
    id: int
    created_at: datetime
    sub_order_to_show: int
    sub_visible: bool
    sub_last_updated: datetime


class SectionResponseBody(CreateSectionRequestBody):
    id: int
    title_slug: str
    created_at: datetime
    order_to_show: int
    visible: bool
    last_updated: datetime

    subsections: list[SubSectionResponseBody] = []

    @validator('subsections', pre=True)
    @classmethod
    def validate_subsections(cls, value):
        if not isinstance(value, list):
            return [value]
        return value
