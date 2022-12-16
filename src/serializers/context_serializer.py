from typing import Any

from enum import StrEnum

from pydantic import BaseModel


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
