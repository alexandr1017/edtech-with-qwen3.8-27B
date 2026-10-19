"""Глобальные настройки приложения."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]


class AppSettings(BaseSettings):
    """Настройки приложения через переменные окружения / .env файл."""

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    ENVIRONMENT: str = "local"
    DATABASE_URL: str | None = None


settings = AppSettings()


def database_url() -> str:
    """Возвращает URL БД из конфигурации или дефолтный SQLite-файл в корне проекта."""
    if settings.DATABASE_URL is not None:
        return settings.DATABASE_URL
    db_path: Path = PROJECT_ROOT / "edtech.db"
    return f"sqlite+aiosqlite:///{db_path}"
