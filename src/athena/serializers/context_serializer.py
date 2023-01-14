from enum import StrEnum


from pydantic import BaseModel, validator


class AlertTypeEnum(StrEnum):
    primary = 'primary'
    secondary = 'secondary'
    success = 'success'
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    light = 'light'
    dark = 'dark'


class DefaultContextSerializer(BaseModel):
    msg: str | None
    alert_type: AlertTypeEnum | None

    @validator('msg', pre=True)
    @classmethod
    def str_to_none_when_empty_string(cls, value: str):
        if not value:
            return None
        return value
