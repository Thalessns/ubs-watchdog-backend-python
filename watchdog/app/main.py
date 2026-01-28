from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from watchdog.database.database import Database
from watchdog.routing.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    await Database.init_models()
    yield


app = FastAPI(title="UBS Watchdog - Python", version="0.0.1", lifespan=lifespan)
prefix = "/api"


@app.get("/", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def root() -> dict[str, str]:
    return {"message": "UBS Watchdog - Python is running!"}


app.include_router(users_router, prefix=prefix)
