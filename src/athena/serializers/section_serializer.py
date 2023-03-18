from datetime import datetime


from pydantic import BaseModel, root_validator

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


class CreateSubSectionRequestBody(BaseModel):
    sub_title: str
    sub_link_image: str | None
    sub_body: str

    @root_validator
    def set_sub_title_slug(cls, root: dict[str, str]):
        root['sub_title_slug'] = slugify(root['sub_title'])
        return root


class SectionResponseBody(CreateSectionRequestBody):
    id: int
    created_at: datetime
    last_updated: datetime


class SubSectionResponseBody(CreateSubSectionRequestBody):
    id: int
    created_at: datetime
    sub_last_updated: datetime
