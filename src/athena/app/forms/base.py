from abc import ABCMeta, abstractmethod

from typing import Any, Generic, TypeVar


from pydantic import BaseModel
from pydantic.fields import ModelField


class BaseForm(BaseModel, metaclass=ABCMeta):

    @classmethod
    def get_form_values(cls):
        return cls.schema()['properties']

    @abstractmethod
    def as_form(cls):
        pass

    class Config:
        allow_population_by_field_name = True


class FormType(Generic[TypeVar('T')]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def _parse_field(cls, field: ModelField):
        to_return = {}
        if not field.field_info.title:
            to_return['title'] = field.name.capitalize()
        if not field.field_info.extra.get('type'):
            to_return['type'] = field.name
        if not field.field_info.extra.get('name'):
            to_return['name'] = field.name
        return to_return

    @classmethod
    def __modify_schema__(
        cls, field_schema: dict[str, Any], field: ModelField | None = None
    ):
        if field:
            field_schema.update(cls._parse_field(field))

    @classmethod
    def validate(cls, value: str, field: ModelField):
        if not isinstance(value, str):
            raise TypeError('str expected')
        return value
