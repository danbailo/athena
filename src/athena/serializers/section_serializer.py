from datetime import datetime


from pydantic import BaseModel, root_validator, Field

from slugify import slugify


class CountSectionResponseBody(BaseModel):
    count: int


class CreateSectionRequestBody(BaseModel):
    title: str
    body: str

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


class SectionResponseBody(CreateSectionRequestBody):
    id: int
    title_slug: str
    created_at: datetime
    last_updated: datetime


class CreateSubSectionRequestBody(BaseModel):
    sub_title: str = Field(..., alias='sub_section_title')
    sub_body: str = Field(..., alias='sub_section_body')
    sub_link_image: str | None = Field(None, alias='sub_section_link_image')

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


class SubSectionResponseBody(CreateSubSectionRequestBody):
    id: int
    created_at: datetime
    sub_last_updated: datetime
