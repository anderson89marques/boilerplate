from collections.abc import AsyncIterable
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from src.app import app



@pytest.fixture
async def client() -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
