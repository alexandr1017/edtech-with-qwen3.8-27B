"""Точка входа FastAPI-приложения."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.config import settings
from src.database import engine
from src.edtech import constants as edtech_constants
from src.edtech import exceptions as edtech_exceptions
from src.edtech.models import Base
from src.edtech.router import router as edtech_router
from src.edtech.web import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание схем БД на старте и закрытие пула при остановке."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


SHOW_DOCS_IN = {"local", "staging"}
app_kwargs: dict[str, object] = {
    "title": "EdTech REST API",
    "lifespan": lifespan,
}
if settings.ENVIRONMENT not in SHOW_DOCS_IN:
    app_kwargs["openapi_url"] = None

app = FastAPI(**app_kwargs)  # type: ignore[arg-type]


_STATUS_BY_CODE: dict[str, int] = {
    edtech_constants.ErrorCode.NOT_FOUND.value: 404,
    edtech_constants.ErrorCode.CONFLICT.value: 409,
}


@app.exception_handler(edtech_exceptions.EdTechError)
async def edtech_error_handler(
    request: Request, exc: edtech_exceptions.EdTechError
) -> JSONResponse:
    """Превращает ошибки домена в HTTP-ответы с каноническими кодами."""
    status_code = _STATUS_BY_CODE.get(exc.code, 500)
    detail = exc.code
    if isinstance(exc, edtech_exceptions.BadActionError):
        detail = f"Allowed actions: {', '.join(exc.allowed)}"
    return JSONResponse(status_code=status_code, content={"error": exc.code, "detail": detail})


@app.get("/health")
async def health() -> dict[str, str]:
    """Проверка живости сервиса."""
    return {"status": "ok"}


app.include_router(edtech_router)
app.include_router(web_router)

STATIC_DIR: Path = Path(__file__).parent / "edtech" / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
