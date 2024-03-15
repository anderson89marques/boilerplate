from asyncio import current_task
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.config import Settings
from src.models.user import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:  # noqa: ARG001
    await startup()
    try:
        yield
    finally:
        await shutdown()


async def startup() -> None:
    create_database()
    logger.info('started...')


async def shutdown() -> None:
    logger.info('...shutdown')


def create_database() -> None:
    engine = create_engine(Settings().DATABASE_URL)
    Base.metadata.create_all(engine)


@asynccontextmanager
async def get_session(self):
    engine = create_async_engine(Settings().DATABASE_URL, echo=False)
    session_factory = async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
        scopefunc=current_task,
    )
    async_session = session_factory()
    try:
        yield async_session
        await async_session.commit()
    except Exception as e:
        logger.exception(f'Session rollback because of exception: {e}')
        await async_session.rollback()
        raise
    finally:
        await async_session.close()
