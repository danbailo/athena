from typing import Any

from enum import StrEnum

from pydantic import BaseModel, validator

from fastapi import Request


class AlertTypeEnum(StrEnum):
    primary = 'primary'
    secondary = 'secondary'
    success = 'success'
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    light = 'light'
    dark = 'dark'


class ContextSerializer(BaseModel):
    request: Any
    msg: str | None
    alert_type: AlertTypeEnum | None

    @validator('request', pre=True)
    @classmethod
    def validate_request_field_type(cls, value: Request):
        if not isinstance(value, Request):
            return ValueError('Invalid type for "request"!')
        return value

    @validator('msg', pre=True)
    @classmethod
    def str_to_none_when_empty_string(cls, value: str):
        if not value:
            return None
        return value
