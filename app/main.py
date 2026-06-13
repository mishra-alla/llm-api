# app/main.py app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup: создаем таблицы БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: закрываем соединения
    await engine.dispose()


def create_app() -> FastAPI:
    """Создание и конфигурация приложения FastAPI"""
    app = FastAPI(
        title=settings.app_name,
        description="FastAPI service with JWT auth, SQLite, and OpenRouter LLM proxy",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация роутеров
    app.include_router(auth_router)
    app.include_router(chat_router)

    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "environment": settings.env}

    return app

app = create_app()