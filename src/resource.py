from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import create_engine

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
    # connect to the database
    logger.info('started...')


async def shutdown() -> None:
    # disconnect from the database
    logger.info('...shutdown')


def create_database() -> None:
    logger.debug("show config")
    engine = create_engine(Settings().DATABASE_URL)
    Base.metadata.create_all(engine)
