from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from watchdog.database.database import Database
from watchdog.routing.clientes.router import clientes_router
from watchdog.routing.transacoes.router import transacoes_router
from watchdog.routing.alertas.router import alertas_router
from watchdog.routing.relatorios.router import relatorio_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    await Database.init_models()
    yield


app = FastAPI(title="UBS Watchdog - Python", version="0.1.0", lifespan=lifespan)


@app.get("/", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def root() -> dict[str, str]:
    return {"message": "UBS Watchdog - Python is running!"}


prefix = "/api"
app.include_router(clientes_router, prefix=prefix)
app.include_router(transacoes_router, prefix=prefix)
app.include_router(alertas_router, prefix=prefix)
app.include_router(relatorio_router, prefix=prefix)
