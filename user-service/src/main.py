from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.database_session import get_engine, create_db_and_tables
from kafka.kafka_producer import flush_kafka_producer
from routers import user_router


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncGenerator:
    print("Preparing DB...")
    engine = get_engine()
    create_db_and_tables(engine)
    yield
    flush_kafka_producer()


app = FastAPI(
    title="user-service",
    lifespan=_lifespan
)

app.include_router(user_router.router)
