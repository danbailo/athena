from contextlib import asynccontextmanager


from fastapi import FastAPI

from database.connection import database

from routers import auth_router, admin_router, user_router, section_router

from extensions.logger import logger
from extensions.env_var import get_env_var


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug('started api')
    await database.connect()
    yield
    logger.debug('shutdown api')
    await database.disconnect()


root_path = get_env_var("API_ROOT_PATH", raise_exception=False) or ""
app = FastAPI(lifespan=lifespan, root_path=root_path)

app.include_router(
    admin_router.router,
    prefix='/admin',
    tags=['admin']
)
app.include_router(
    auth_router.router,
    prefix='/auth',
    tags=['auth']
)
app.include_router(
    user_router.router,
    prefix='/user',
    tags=['user']
)
app.include_router(
    section_router.router,
    prefix='/section',
    tags=['section']
)
