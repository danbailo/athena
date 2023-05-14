import asyncio

from functools import wraps


from sqlalchemy import insert

import typer


from database.models.user_model import UserModel, RoleEnum
from database.connection import database

from extensions.logger import logger

from utils.auth_util import get_password_hash


app = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@app.callback()
def callback():
    pass


@app.command()
@coro
async def create_admin_user(
    name: str = typer.Option(),
    username: str = typer.Option(),
    email: str = typer.Option(),
    password: str = typer.Option()
):
    logger.info('iniciando aplicacao')
    password_hash = get_password_hash(password)
    query = insert(UserModel).values(
        name=name,
        username=username,
        email=email,
        password_hash=password_hash,
        role=RoleEnum.admin)
    await database.connect()
    try:
        await database.execute(query)
    except Exception as exc:
        logger.critical(exc, exc_info=True)
    await database.disconnect()
    logger.info('aplicacao finalizada')


if __name__ == '__main__':
    app()
