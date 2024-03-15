from asyncio import current_task
from collections.abc import AsyncIterable

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import configure_mappers, sessionmaker

from src.app import app
from src.models.user import Base, User
from src.resources import get_session


@pytest.fixture
async def session():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=False)
    session_factory = async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
        scopefunc=current_task,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with session_factory(bind=connection) as session:
            configure_mappers()
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
async def client(session) -> AsyncIterable[AsyncClient]:
    async def get_session_override():
        yield session

    async with AsyncClient(app=app, base_url='http://test') as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def user(session):
    user = User(
        username='alice', email='alice@example.com', password='testtest'
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
