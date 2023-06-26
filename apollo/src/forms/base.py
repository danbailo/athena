from abc import ABCMeta, abstractmethod

from typing import Any, Generic, TypeVar


from pydantic import BaseModel
from pydantic.fields import ModelField

from datetime import datetime


class BaseForm(BaseModel, metaclass=ABCMeta):

    @classmethod
    def get_form_fields(cls):
        return cls.schema(by_alias=True)['properties']

    @classmethod
    @abstractmethod
    def as_form(cls):
        pass

    def get_form_values(self):
        fields = self.get_form_fields()
        return {key: {'form': fields[key],
                      'value': getattr(self, key)}
                for key in self.dict().keys()}

    class Config:
        allow_population_by_field_name = True


# https://docs.pydantic.dev/latest/usage/schema/#modifying-schema-in-custom-fields
class FormType(Generic[TypeVar('T')]):

    @classmethod
    def _parse_fields(
        cls, field_schema: dict[str, Any], field: ModelField | None = None
    ):
        pass

    @classmethod
    def __modify_schema__(
        cls, field_schema: dict[str, Any], field: ModelField | None = None
    ):
        field_schema.update(
            {'class': 'form-control', 'name': field.name, 'form_value': True})
        field_schema.update(field.field_info.extra)
        default_title =\
            getattr(field.field_info, 'title', None) or field.name.capitalize()
        field_schema.setdefault('title', default_title)
        field_schema.setdefault('type', 'text')
        field_schema.setdefault('id', field.name)
        cls._parse_fields(field_schema, field)


class BooleanType(FormType[bool]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: bool, field: ModelField):
        if not isinstance(value, bool):
            raise TypeError('bool expected')
        return value

    @classmethod
    def _parse_fields(
        cls, field_schema: dict[str, Any], field: ModelField | None = None
    ):
        field_schema.update({
            'type': 'checkbox',
            'class': 'form-check-input',
            'onclick': 'sendValueCheckboxUsingHide(this.id)'})


class IntegerType(FormType[int]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: int, field: ModelField):
        if not isinstance(value, int):
            raise TypeError('int expected')
        return value

    @classmethod
    def _parse_fields(
        cls, field_schema: dict[str, Any], field: ModelField | None = None
    ):
        field_schema.update({'type': 'number'})


class StringType(FormType[str]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str, field: ModelField):
        if not isinstance(value, str):
            raise TypeError('str expected')
        return value


class DateTimeType(FormType[datetime]):
    @classmethod
    def __get_validators__(cls):
        yield cls.format_value
        yield cls.validate

    @classmethod
    def format_value(cls, value: str):
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')

    @classmethod
    def validate(cls, value: datetime, field: ModelField):
        if not isinstance(value, datetime):
            raise TypeError('datetime expected')
        return value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    @classmethod
    def _parse_fields(
        cls, field_schema: dict[str, Any], field: ModelField | None = None
    ):
        field_schema.update({'type': 'datetime-local', 'step': '0.001'})
