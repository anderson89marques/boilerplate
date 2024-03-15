from collections.abc import AsyncIterable
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import app
from src.models.user import Base


@pytest.fixture
async def client() -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)