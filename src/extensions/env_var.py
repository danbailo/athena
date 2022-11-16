import os


from dotenv import load_dotenv

from .logger import logger

load_dotenv()


def get_env_var(key: str, raise_exception: bool = False) -> str | None:
    if not (value := os.getenv(key)) and raise_exception is True:
        raise ValueError('variable does not exists in env!')
    elif value is None and raise_exception is False:
        logger.warning(
            f'variable not declared in the environment - {key.upper()}'
        )
    return value
