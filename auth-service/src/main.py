from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.database_session import get_engine, create_db_and_tables
from routers import user_router, auth_router


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncGenerator:
    print("Preparing DB...")
    engine = get_engine()
    create_db_and_tables(engine)
    yield


app = FastAPI(
    title="auth-service",
    lifespan=_lifespan
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
