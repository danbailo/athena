import os

from typing import Any


from dotenv import load_dotenv

from .logger import logger

load_dotenv()


ATHENA_PROJECT_VARS = {}


def set_project_var(key: Any, value: Any) -> Any:
    ATHENA_PROJECT_VARS[key] = value
    return value


def get_env_var(key: str, raise_exception: bool = True) -> str | None:
    if not (value := (
        os.environ.get(key) or ATHENA_PROJECT_VARS.get(key))
    ) and raise_exception is True and value is None:
        raise ValueError('variable does not exists in env!')
    if value is None and raise_exception is False:
        logger.warning(
            'variable not declared in the environment - %s', key.upper()
        )
    return value
