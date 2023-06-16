from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import database

from routers import auth_router, admin_router, user_router, section_router

from extensions.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug('started api')
    await database.connect()
    yield
    logger.debug('shutdown api')
    await database.disconnect()


app = FastAPI(lifespan=lifespan, root_path='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost',
        'http://localhost:8001',
        'https://localhost',
        'https://localhost:8001',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

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
