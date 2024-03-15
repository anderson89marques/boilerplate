from fastapi import FastAPI
from src.routers.user import router as user_router
from src.routers.hello_world import router as hello_router
from src.resources import lifespan

app = FastAPI(
    title="Boilerplate Fastapi Project",
    lifespan=lifespan,
)

routers = (
    user_router,
    hello_router
)

for router in routers:
    app.include_router(router)
