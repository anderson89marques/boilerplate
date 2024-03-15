from fastapi import FastAPI
from src.routers.user import router as user_router

app = FastAPI(
    title="Boilerplate Fastapi Project"
)

app.include_router(user_router)

@app.get('/')
async def say_hello() -> dict[str, str]:
    return {'message': 'Hello World'}
